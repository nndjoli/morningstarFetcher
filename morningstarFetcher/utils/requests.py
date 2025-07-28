"""HTTP helpers shared by the screener and security modules."""

from __future__ import annotations

import asyncio
from functools import lru_cache
from typing import Any, Dict

import httpx
import ua_generator


def _base_headers() -> Dict[str, str]:
    return {
        "User-Agent": ua_generator.generate(device="desktop", browser=("chrome", "edge")).text,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "referer": "https://www.morningstar.com/",
    }


@lru_cache(maxsize=1)
def get_token() -> str:
    """Retrieve an access token from Morningstar."""
    resp = httpx.get(
        "https://www.morningstar.com/api/v2/stores/maas/token", headers=_base_headers()
    )
    if resp.status_code != 200:
        raise RuntimeError(
            f"Failed to retrieve token: {resp.status_code}"
        )
    text = resp.text.strip()
    if not text:
        raise RuntimeError("Empty token received from Morningstar")
    return text


def request_headers() -> Dict[str, str]:
    token = get_token()
    headers = _base_headers()
    headers["authorization"] = f"Bearer {token}"
    headers["apikey"] = "lstzFDEOhfFNMLikKa0am9mgEKLBl49T"
    headers["x-api-realtime-e"] = (
        "eyJlbmMiOiJBMTI4R0NNIiwiYWxnIjoiUlNBLU9BRVAifQ.X-h4zn65XpjG8cZnL3e6hj8LMbzupQBglHZce7tzu-c4utCtXQ2IYoLxdik04usYRhNo74AS_2crdjLnBc_J0lFEdAPzb_OBE7HjwfRaYeNhfXIDw74QCrFGqQ5n7AtllL-vTGnqmI1S9WJhSwnIBe_yRxuXGGbIttizI5FItYY.bB3WkiuoS1xzw78w.iTqTFVbxKo4NQQsNNlbkF4tg4GCfgqdRdQXN8zQU3QYhbHc-XDusH1jFii3-_-AIsqpHaP7ilG9aBxzoK7KPPfK3apcoMS6fDM3QLRSZzjkBoxWK75FtrQMAN5-LecdJk97xaXEciS0QqqBqNugoSPwoiZMazHX3rr7L5jPM-ecXN2uEjbSR0wfg-57iHAku8jvThz4mtGpMRAOil9iZaL6iRQ.o6tR6kuOQBhnpcsdTQeZWw"
    )
    return headers


class QueryManager:
    """Simple synchronous HTTP client using shared headers."""

    def __init__(self) -> None:
        self.headers = request_headers()
        self.client = httpx.Client(headers=self.headers)

    def get(self, url: str, output: str = "json") -> Any:
        resp = self.client.get(url)
        if output == "json":
            return resp.json()
        return resp.text


async def async_get(url: str, headers: Dict[str, str] | None = None) -> Any:
    headers = headers or request_headers()
    async with httpx.AsyncClient(headers=headers, timeout=30.0) as client:
        resp = await client.get(url)
        if resp.status_code == 200:
            try:
                return resp.json()
            except Exception:
                return {"error": f"Failed to parse JSON from {url}"}
        return {"error": f"Failed to fetch {url}: {resp.status_code}"}


async def async_gather(tasks: Dict[str, str], headers: Dict[str, str] | None = None) -> Dict[str, Any]:
    """Fetch multiple URLs concurrently and return a name->json mapping."""

    headers = headers or request_headers()
    async with httpx.AsyncClient(headers=headers, timeout=30.0) as client:
        coros = {name: client.get(url) for name, url in tasks.items()}
        responses = await asyncio.gather(*coros.values())
    results: Dict[str, Any] = {}
    for key, resp in zip(coros.keys(), responses):
        if resp.status_code == 200:
            try:
                results[key] = resp.json()
            except Exception:
                results[key] = {"error": f"Failed to parse JSON from {resp.url}"}
        else:
            results[key] = {"error": f"Failed to fetch {resp.url}: {resp.status_code}"}
    return results
