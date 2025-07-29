from __future__ import annotations

import asyncio
from typing import Any, Dict, List, Sequence

import httpx
import pandas as pd

from .utils.async_helpers import run_async
from .utils.filtering import build_filter_string
from .utils.requests import request_headers
from .utils.screener_utils import get_market, process_markets_response, process_query_response, screener_builders, universe_fields

__all__ = ["Screener"]

_INV_TYPE_TO_CODE: Dict[str, str] = {
    "stocks": "EQ",
    "etfs": "FE",
    "mutual_funds": "FO",
}
_CODE_TO_INV_TYPE: Dict[str, str] = {v: k for k, v in _INV_TYPE_TO_CODE.items()}


class Screener:
    """High-level helper around the Morningstar global screener endpoint.

    Field names are aggregated from the ``views`` and ``fields`` metadata stores.
    The :py:meth:`get` method exposes all available data points.
    """

    country_codes: Dict[str, Any]
    """dict: Raw country code metadata from Morningstar."""

    processed_markets: Dict[str, Any]
    """dict: Markets indexed by ID for quick lookup."""

    def __init__(self) -> None:
        self._headers = request_headers()
        self._builders = run_async(screener_builders(self._headers))
        self.country_codes = self._builders["country_codes"]

        self._editions = self._builders["editions"]
        self._markets_response = self._builders["markets"]
        self._languages = self._builders["languages"]
        self._fields_response = self._builders["fields"]
        self._views_response = self._builders["views"]
        self._documents = self._builders["documents"]

        # Store processed market metadata for quick lookups
        self.processed_markets = process_markets_response(self._markets_response)

        # ``markets`` exposes a simplified mapping of ID -> display name
        self.markets = {mid: info.get("displayName", mid) for mid, info in self.processed_markets.items()}
        self.stocks_fields = universe_fields(self._fields_response, universe_id=_INV_TYPE_TO_CODE["stocks"])
        self.etfs_fields = universe_fields(self._fields_response, universe_id=_INV_TYPE_TO_CODE["etfs"])
        self.mutual_funds_fields = universe_fields(
            self._fields_response,
            universe_id=_INV_TYPE_TO_CODE["mutual_funds"],
        )

    def get(
        self,
        investment_type: str,
        market_id: str,
        sort_by: str = "totalReturn[ytd]:desc",
        pages: int = 1,
        filters: Sequence[Sequence[str]] | None = None,
        logs: bool = False,
    ) -> pd.DataFrame:
        """Return screener results for the given market and universe.

        Parameters
        ----------
        investment_type : str
            Asset universe to query. Must be one of ``{"stocks", "etfs", "mutual_funds"}``.
        market_id : str
            Identifier of the market as defined in :pyattr:`processed_markets`.
        sort_by : str, optional
            Sort field and direction in the form ``"field:asc"`` or
            ``"field:desc"``. Default is ``"totalReturn[ytd]:desc"``.
        pages : int, optional
            Number of 500-row pages to retrieve. Must be ``>= 1``. Defaults to
            ``1``.
        filters : Sequence[Sequence[str]], optional
            List of ``(field, operator, value)`` tuples to append to the query.
            Wildcard characters ``*`` and ``?`` are automatically translated to
            SQL wildcards.
        logs : bool, optional
            If ``True`` every underlying HTTP request URL is printed. Defaults
            to ``False``.
        Returns
        -------
        pandas.DataFrame
            One row per security matching the criteria.
        """
        # Validate inputs
        if investment_type not in _INV_TYPE_TO_CODE:
            raise ValueError(f"Unknown investment_type '{investment_type}'. Must be one of: {_INV_TYPE_TO_CODE.keys()}")
        inv_code = _INV_TYPE_TO_CODE[investment_type]
        if market_id not in self.markets:
            raise ValueError(f"Unknown market_id '{market_id}'. Must be one of: {list(self.markets.keys())}")
        if pages < 1 or not isinstance(pages, int):
            raise ValueError("'pages' must be an integer ≥ 1.")

        # Retrieve full market information from the processed metadata
        market = get_market(market_id, self.processed_markets)
        query_info = market["queries"].get(inv_code)
        if not query_info:
            raise ValueError(f"Universe '{investment_type}' not in market '{market_id}'. Must be one of: {list(market['queries'].keys())}")
        query_base = query_info["query"]

        # Resolve fields & sort
        all_fields_map = universe_fields(self._fields_response, universe_id=inv_code)
        all_fields = list(all_fields_map.keys())

        sort_field = sort_by.split(":")[0]
        if sort_field not in all_fields:
            raise ValueError(f"Sort field '{sort_field}' not among fields. Must be one of: {all_fields}")

        # Combine query
        query_string = query_base
        if filters:
            fields_map = {
                "stocks": self.stocks_fields,
                "etfs": self.etfs_fields,
                "mutual_funds": self.mutual_funds_fields,
            }
            filter_string = build_filter_string(filters, fields_map[investment_type])
            if filter_string:
                query_string = f"{query_base} AND {filter_string}"

        base_url = "https://global.morningstar.com/api/v1/en-eu/tools/screener/_data"

        field_batch_size = 99

        field_batches: List[List[str]] = [all_fields[i : i + field_batch_size] for i in range(0, len(all_fields), field_batch_size)]

        if logs:
            print(f"Query: {query_string}")
            print(f"Sort by: {sort_by}")
            print(f"Fields: {len(all_fields)} ({field_batch_size} per batch)")

        if logs:
            for i, batch in enumerate(field_batches):
                print(f"Batch {i + 1}/{len(field_batches)}: {len(batch)} fields")

        if logs:
            print(f"Total pages: {pages}")

        async def _fetch(batch: Sequence[str]) -> List[Dict[str, Any]]:
            async with httpx.AsyncClient(headers=self._headers) as client:
                tasks = [
                    client.get(
                        base_url,
                        params={
                            "query": query_string,
                            "fields": ",".join(batch),
                            "page": p,
                            "sort": sort_by,
                            "limit": 500,
                        },
                    )
                    for p in range(1, pages + 1)
                ]
                responses = await asyncio.gather(*tasks)

            records: List[Dict[str, Any]] = []
            for r in responses:
                if r.status_code != 200:
                    raise RuntimeError(f"{r.status_code} — {r.url}: {r.text[:200]}")
                if logs:
                    print(f"Fetched {r.url}")
                records.extend(process_query_response(r.json()))
            return records

        frames: List[pd.DataFrame] = []
        for batch in field_batches:
            batch_records = run_async(_fetch(batch))
            df_batch = pd.DataFrame(batch_records)
            for col in df_batch.columns:
                if logs:
                    if "ID" in col or "id" in col:
                        print(f"ID Col: {col}")
            df_batch = df_batch.set_index("securityID")
            frames.append(df_batch)

        combined = pd.concat(frames, axis=1)
        combined = combined.loc[:, ~combined.columns.duplicated()].reset_index()
        return combined
