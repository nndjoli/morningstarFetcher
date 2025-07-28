"""Load query string templates for each security type."""

from . import etf_queries, fund_queries, stock_queries


class QueryStringsManager:
    """Provide lists of URLs for ETF, Stock and Fund requests."""

    def __init__(self, today: str | None = None) -> None:
        self.etf_links = etf_queries.get_queries(today=today)
        self.stock_links = stock_queries.get_queries(today=today)
        self.fund_links = fund_queries.get_queries(today=today)


__all__ = ["QueryStringsManager"]
