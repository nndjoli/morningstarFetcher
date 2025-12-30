from __future__ import annotations

from typing import Any, Dict, Iterable, List, Sequence

import httpx
import pandas as pd

from .utils.async_helpers import run_async
from .utils.requests import request_headers
from .utils.screener_utils import screener_builders

__all__ = ["Search"]

_DEFAULT_FIELDS: Sequence[str] = (
    "baseCurrency",
    "dgsCode",
    "exchange",
    "exchangeCountry",
    "fundServCodes",
    "isin",
    "itaCode",
    "marketCap",
    "name",
    "shortName",
    "ticker",
)

_ORDERED_COLUMNS: Sequence[str] = (
    "name",
    "shortName",
    "isin",
    "securityID",
    "performanceID",
    "fundID",
    "masterPortfolioID",
    "universe",
    "baseCurrency",
    "score",
)

_DEFAULT_EXCHANGE_COUNTRIES: List[str] = [
    "AUT",
    "BEL",
    "CHE",
    "DEU",
    "ESP",
    "FRA",
    "GBR",
    "IRL",
    "ITA",
    "LUX",
    "NLD",
    "PRT",
    "DNK",
    "FIN",
    "NOR",
    "SWE",
]


class _SearchFactory(type):
    """Metaclass enabling ``Search(term)`` convenience calls."""

    def __call__(
        cls,
        term: str | None = None,
        country: str = "FRA",
        *,
        fields: Sequence[str] | None = None,
        limit: int = 50,
        page: int = 1,
        sort: str = "_score",
        locale: str | None = None,
        _as_client: bool = False,
    ):
        if _as_client:
            return super().__call__(locale=locale or "fr")
        if term is None:
            raise TypeError("Search requires a term when called directly. Use Search.client(...) for a reusable instance.")
        client = super().__call__(locale=locale or "fr")
        return client.search(term, country=country, fields=fields, limit=limit, page=page, sort=sort, locale=locale)


class Search(metaclass=_SearchFactory):
    """Lightweight helper around the Morningstar search endpoint.

    The class is callable: ``Search("Sycomore")`` runs a one-off search and returns
    a :class:`pandas.DataFrame` with flattened results, including ``securityID`` and
    the requested metadata fields.

    Examples
    --------
    Quick one-off:
    >>> import morningstarFetcher as ms
    >>> df = ms.Search("Sycomore")
    >>> df[["securityID", "isin", "name"]].head()

    Reusable client with custom locale:
    >>> client = ms.Search.client(locale="fr")
    >>> df = client("Sycomore", country="FRA", limit=100)
    >>> df2 = client("Apple", country="USA", fields=["isin", "ticker", "name"])
    """

    def __init__(self, locale: str = "fr") -> None:
        self.locale = (locale or "fr").strip("/") or "fr"
        self._headers = self._init_headers()
        self._country_codes = self._load_country_codes()
        self._all_countries: List[str] = list(self._country_codes.get("ALL_COUNTRY_CODES", []))

    @classmethod
    def client(cls, locale: str = "fr") -> "Search":
        """Return a reusable Search client without performing a request."""
        return cls(term=None, _as_client=True, locale=locale)

    @staticmethod
    def _init_headers() -> Dict[str, str] | None:
        try:
            return request_headers()
        except Exception:
            # If token retrieval fails we still attempt the call without custom headers.
            return None

    def _load_country_codes(self) -> Dict[str, Any]:
        try:
            builders = run_async(screener_builders(self._headers))
        except Exception:
            return {}
        return builders.get("country_codes", {}) or {}

    def _normalize_country(self, country: str) -> str:
        code = (country or "").upper()
        if not code:
            raise ValueError("Country code cannot be empty.")
        if self._all_countries and code not in self._all_countries:
            raise ValueError(f"Unknown country code '{code}'. Must be one of: {self._all_countries}")
        return code

    def _exchange_countries(self, country: str) -> List[str]:
        pool: Iterable[str] = (
            self._country_codes.get("CENTRAL_EUROPE_NORDICS")
            or self._country_codes.get("ALL_COUNTRY_CODES")
            or _DEFAULT_EXCHANGE_COUNTRIES
        )
        pool_list = list(pool)
        if country not in pool_list:
            pool_list = [country] + [c for c in pool_list if c != country]
        return pool_list

    def _build_query(self, term: str, country: str) -> str:
        safe_term = (term or "").replace('"', '\\"')
        exchange_countries = ",".join(f'"{code}"' for code in self._exchange_countries(country))
        return (
            f'((isin ~= "{safe_term}" '
            f'OR ticker ~= "{safe_term}" '
            f'OR name ~= "{safe_term}" '
            f'OR companyName ~= "{safe_term}" '
            f'OR isin ~= "{safe_term}") '
            "AND ("
            '(investmentType = "EQ") '
            f'OR (investmentType = "FC" AND countriesOfSale = "{country}") '
            f'OR (investmentType = "FE" AND exchangeCountry in ({exchange_countries})) '
            f'OR (investmentType = "FO" AND countriesOfSale = "{country}") '
            'OR (investmentType = "XI")'
            "))"
        )

    def _flatten_results(self, payload: Dict[str, Any]) -> pd.DataFrame:
        records: List[Dict[str, Any]] = []
        for item in payload.get("results", []) or []:
            record: Dict[str, Any] = {}
            record.update(item.get("meta", {}))
            for field_name, content in (item.get("fields") or {}).items():
                if isinstance(content, dict):
                    if "value" in content:
                        record[field_name] = content.get("value")
                    for extra_key, extra_value in content.items():
                        if extra_key != "value":
                            record[f"{field_name}_{extra_key}"] = extra_value
                else:
                    record[field_name] = content
            if "score" in item:
                record["score"] = item.get("score")
            records.append(record)
        df = pd.DataFrame(records)

        # Reorder columns to keep key identifiers first, preserving any extras afterward.
        leading = [col for col in _ORDERED_COLUMNS if col in df.columns]
        rest = [c for c in df.columns if c not in leading]
        return df[leading + rest]

    def search(
        self,
        term: str,
        country: str = "FRA",
        *,
        fields: Sequence[str] | None = None,
        limit: int = 50,
        page: int = 1,
        sort: str = "_score",
        locale: str | None = None,
    ) -> pd.DataFrame:
        """Search securities and return a dataframe with identifiers and fields.

        Parameters
        ----------
        term : str
            Search term matched against ISIN, ticker, name, or companyName.
        country : str, optional
            3-letter country code used for country-aware filters (default: ``"FRA"``).
        fields : Sequence[str], optional
            Additional fields to request. Defaults to a curated set that includes
            ``baseCurrency``, ``exchange``, ``isin``, ``name``, and related identifiers.
        limit : int, optional
            Maximum rows to fetch (default: 50).
        page : int, optional
            Page index for pagination (default: 1).
        sort : str, optional
            Sort field, defaults to ``"_score"``.
        locale : str, optional
            Locale path segment for the endpoint (e.g., ``"fr"`` or ``"en-eu"``).

        Returns
        -------
        pandas.DataFrame
            Flattened search results with ``securityID`` and requested fields.
        """

        country_code = self._normalize_country(country)
        search_fields = fields or _DEFAULT_FIELDS
        params = {
            "fields": ",".join(search_fields),
            "limit": limit,
            "page": page,
            "query": self._build_query(term, country_code),
            "sort": sort,
        }
        base_locale = (locale or self.locale).strip("/") or "fr"
        url = f"https://global.morningstar.com/api/v1/{base_locale}/search/securities"
        response = httpx.get(url, params=params, headers=self._headers)
        if response.status_code != 200:
            raise RuntimeError(f"Search request failed ({response.status_code}): {response.text[:200]}")
        return self._flatten_results(response.json())

    def __call__(
        self,
        term: str,
        country: str = "FRA",
        *,
        fields: Sequence[str] | None = None,
        limit: int = 50,
        page: int = 1,
        sort: str = "_score",
        locale: str | None = None,
    ) -> pd.DataFrame:
        """Allow calling the instance like a function."""
        return self.search(term, country=country, fields=fields, limit=limit, page=page, sort=sort, locale=locale)
