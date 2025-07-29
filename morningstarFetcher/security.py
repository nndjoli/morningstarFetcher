from dataclasses import dataclass

from .queries import etf_queries, fund_queries, stock_queries
from .utils.async_helpers import run_async
from .utils.requests import QueryManager as query_manager
from .utils.requests import async_gather, request_headers


def get_metadata(query_manager, security_id):
    security_metadata_url = "https://api-global.morningstar.com/sal-service/v1/fund/securityMetaData/<SECURITY_ID>"
    security_metadata_response = query_manager.get(security_metadata_url.replace("<SECURITY_ID>", security_id))
    security_metadata_keys = [
        "secId",
        "fundId",
        "name",
        "tradingSymbol",
        "performanceId",
        "masterPortfolioId",
        "isin",
        "securityType",
        "shortCountryId",
        "categoryId",
        "domicileCountryId",
        "fundShareClassId",
        "baseCurrencyId",
        "countryId",
    ]
    security_metadata_dict = {key: security_metadata_response.get(key, None) for key in security_metadata_keys}
    return security_metadata_dict


async def queries(tasks, headers=None):
    return await async_gather(tasks, headers=headers)


class LazyFetchClass:
    """Class providing lazy-loading behavior for security data."""

    _lazy: bool = False
    __tasks__: dict
    __req_h__: dict

    def __getattribute__(self, name):
        # Always allow access to internal attributes without interception
        if name.startswith("_") or name in {"__tasks__", "_lazy", "_fetch_attribute"}:
            return object.__getattribute__(self, name)

        lazy = object.__getattribute__(self, "_lazy") if "_lazy" in self.__dict__ else False
        if lazy:
            tasks = object.__getattribute__(self, "__tasks__")
            if name in tasks:
                instance_dict = object.__getattribute__(self, "__dict__")
                if name not in instance_dict or instance_dict.get(name) is None:
                    self._fetch_attribute(name)
        return object.__getattribute__(self, name)

    def _fetch_attribute(self, name):
        url = self.__tasks__[name]
        result = run_async(queries({name: url}, headers=self.__req_h__))
        setattr(self, name, result.get(name))


@dataclass
class ETF(LazyFetchClass):
    disclosure_flag: dict = None
    """dict: Regulatory disclosure flags for the ETF."""

    distribution_annual: dict = None
    """dict: Annual distribution data in base currency."""

    distribution_latest: dict = None
    """dict: Most recent distribution details."""

    esg_risk: dict = None
    """dict: ESG risk metrics."""

    esg_product_involvement: dict = None
    """dict: ESG product involvement breakdown."""

    factor_exposure_profile: dict = None
    """dict: Factor exposure profile."""

    investment_strategy: dict = None
    """dict: Morningstar investment strategy commentary."""

    fixed_income_exposure: dict = None
    """dict: Fixed-income exposure details by region and sector."""

    parent_fund_flow: dict = None
    """dict: Parent fund flow graph data."""

    parent_medalist_rating_summary: dict = None
    """dict: Medalist rating summary for the parent fund."""

    parent_medalist_rating_top_funds: dict = None
    """dict: Top funds ranked by medalist rating."""

    parent_medalist_rating_top_funds_up_down: dict = None
    """dict: Medalist rating flows up/down for top funds."""

    parent_fund_star_ratings_asc: dict = None
    """dict: Parent fund star ratings (ascending)."""

    parent_fund_star_ratings_desc: dict = None
    """dict: Parent fund star ratings (descending)."""

    parent_fund_overall_star_rating: dict = None
    """dict: Overall parent fund star rating."""

    parent_fund_summary: dict = None
    """dict: Summary information about the parent fund."""

    market_volatility_measure_10y: dict = None
    """dict: Ten-year market volatility measures."""

    market_volatility_measure_3y: dict = None
    """dict: Three-year market volatility measures."""

    market_volatility_measure_5y: dict = None
    """dict: Five-year market volatility measures."""

    risk_return_scatterplot: dict = None
    """dict: Data for the risk/return scatter plot."""

    risk_return_summary: dict = None
    """dict: Summary metrics of risk versus return."""

    risk_score: dict = None
    """dict: Risk score values."""

    risk_volatility: dict = None
    """dict: Volatility measures used for risk analysis."""

    performance_table: dict = None
    """dict: Performance table of annual returns."""

    performance_10k_growth: dict = None
    """dict: Growth of 10k and related performance data."""

    portfolio_holdings: dict = None
    """dict: Portfolio holdings details."""

    portfolio_regional_sector_exposure: dict = None
    """dict: Regional sector exposure breakdown."""

    portfolio_regional_sector_include_countries: dict = None
    """dict: Regional and country sector exposures."""

    portfolio_sector_exposure: dict = None
    """dict: Sector exposure using v2 endpoint."""

    price_cost_projection: dict = None
    """dict: Projected costs over time."""

    price_fee_level: dict = None
    """dict: Fee level classification."""

    price: dict = None
    """dict: Latest price information."""

    process_asset_allocation: dict = None
    """dict: Asset allocation data."""

    process_equity_style_box_history: dict = None
    """dict: Historical equity style box positions."""

    process_financial_metrics: dict = None
    """dict: Key financial metrics."""

    process_market_capitalization: dict = None
    """dict: Market capitalization breakdown."""

    process_ownership_zone: dict = None
    """dict: Ownership zone statistics."""

    process_stock_style: dict = None
    """dict: Stock style information."""

    process_weighting: dict = None
    """dict: Portfolio weighting by style."""

    quote_mini_chart_realtime_data: dict = None
    """dict: Real-time mini chart price data."""

    quote_investment_overview: dict = None
    """dict: Investment overview quote data."""

    quote: dict = None
    """dict: Full quote information."""

    history_dividend_monthly: dict = None
    """dict: Monthly dividend history."""

    history_market_total_return_daily: dict = None
    """dict: Daily market total return history."""

    history_price_monthly: dict = None
    """dict: Monthly price history."""

    history_premium_discount_monthly: dict = None
    """dict: Monthly premium/discount history."""

    history_price_daily: dict = None
    """dict: Daily price history."""

    market_id_information: dict = None
    """dict: Additional market identifier information."""

    def __init__(self, security_id, lazy: bool = False):
        self.security_id = security_id
        # Lazy loading can't be enabled until __tasks__ is populated. Set to
        # False during initialization to avoid attribute errors from
        # ``__getattribute__``.
        self._lazy = False
        self.__qm__ = query_manager()
        self.__req_h__ = request_headers()

        if not security_id:
            raise ValueError("Security ID cannot be empty.")

        self.security_metadata = get_metadata(self.__qm__, self.security_id)
        self.security_type = self.security_metadata.get("securityType", None)

        if self.security_type is None:
            raise ValueError("Security type not found in metadata.")

        if self.security_type != "FE":
            raise ValueError("Incompatible security type.")

        self.queries_urls = [
            {
                "name": q["name"],
                "url": q["url"].replace("<ETF_ID>", self.security_metadata["secId"]),
            }
            for q in etf_queries.get_queries()
        ]

        self.__tasks__ = {item["name"]: item["url"] for item in self.queries_urls}
        # ``_lazy`` is only set to the requested value once all required
        # attributes are initialized and ``__tasks__`` is available.
        self._lazy = lazy

        if not self._lazy:
            result = run_async(queries(self.__tasks__, headers=self.__req_h__))
            for k, v in result.items():
                setattr(self, k, v)
        else:
            for k in self.__tasks__:
                setattr(self, k, None)


@dataclass
class Stock(LazyFetchClass):
    company_profile: dict = None
    """dict: Basic company profile information."""

    dividends: dict = None
    """dict: Historical dividend payments."""

    equity_overview: dict = None
    """dict: Overview of the company's equity metrics."""

    esg_risk_rating_assessment: dict = None
    """dict: ESG risk rating assessment data."""

    esg_risk_rating_breakdown: dict = None
    """dict: Detailed ESG risk rating breakdown."""

    insiders_board_of_directors: dict = None
    """dict: List of board of directors."""

    insiders_key_executives: dict = None
    """dict: Key executive information."""

    insiders_transaction_chart: dict = None
    """dict: Insider transaction chart data."""

    insiders_transaction_history: dict = None
    """dict: Historical insider transactions."""

    key_metrics_cashflow: dict = None
    """dict: Cash flow key metrics."""

    key_metrics_financial_health: dict = None
    """dict: Financial health key metrics."""

    key_metrics_profitability_and_efficiency: dict = None
    """dict: Profitability and efficiency metrics."""

    key_metrics_summary: dict = None
    """dict: Summary of key financial metrics."""

    key_stats_growth_table: dict = None
    """dict: Growth statistics table."""

    quote_mini_chart_realtime_data: dict = None
    """dict: Real-time mini chart data."""

    financials_balance_sheet_annual: dict = None
    """dict: Annual balance sheet data."""

    financials_balance_sheet_quarterly: dict = None
    """dict: Quarterly balance sheet data."""

    financials_cash_flow_annual: dict = None
    """dict: Annual cash flow statements."""

    financials_cash_flow_quarterly: dict = None
    """dict: Quarterly cash flow statements."""

    financials_income_statement_annual: dict = None
    """dict: Annual income statement data."""

    financials_income_statement_quarterly: dict = None
    """dict: Quarterly income statement data."""

    ownership_institutional_buyers: dict = None
    """dict: Institutional buyers."""

    ownership_mutual_fund_buyers: dict = None
    """dict: Mutual fund buyers."""

    ownership_concentrated_institutional_owners: dict = None
    """dict: Concentrated institutional owners."""

    ownership_concentrated_mutual_fund_owners: dict = None
    """dict: Concentrated mutual fund owners."""

    ownership_institutional: dict = None
    """dict: Ownership data for institutions."""

    ownership_mutual_fund: dict = None
    """dict: Ownership data for Mutual Funds."""

    ownership_institutional_sellers: dict = None
    """dict: Institutional sellers."""

    ownership_mutual_fund_sellers: dict = None
    """dict: Mutual fund sellers."""

    realtime_quote: dict = None
    """dict: Real-time quote information."""

    splits: dict = None
    """dict: Stock split history."""

    trading_information: dict = None
    """dict: Trading information such as volume and exchange."""

    trailing_total_returns_daily: dict = None
    """dict: Trailing total returns on a daily basis."""

    trailing_total_returns_monthly: dict = None
    """dict: Trailing total returns on a monthly basis."""

    trailing_total_returns_quarterly: dict = None
    """dict: Trailing total returns on a quarterly basis."""

    valuation: dict = None
    """dict: Valuation metrics for the stock."""

    history_rolling_eps_monthly: dict = None
    """dict: Monthly rolling EPS history."""

    history_rolling_eps_short_interest_ratio_monthly: dict = None
    """dict: Monthly rolling EPS and short interest ratio history."""

    history_price_to_book_price_to_cash_flow_monthly: dict = None
    """dict: Monthly price-to-book and price-to-cash-flow history."""

    history_price_to_cash_flow_monthly: dict = None
    """dict: Monthly price-to-cash-flow history."""

    history_pe_ratio_monthly: dict = None
    """dict: Monthly price/earnings ratio history."""

    history_pe_ratio_price_to_sales_monthly: dict = None
    """dict: Monthly P/E and price-to-sales history."""

    history_price_to_sales_price_to_book_monthly: dict = None
    """dict: Monthly price-to-sales and price-to-book history."""

    history_dividends_earnings_splits_monthly: dict = None
    """dict: Monthly dividends, earnings and splits history."""

    history_market_total_return_monthly: dict = None
    """dict: Monthly market total return history."""

    history_price_daily: dict = None
    """dict: Daily price history."""

    history_price_monthly: dict = None
    """dict: Monthly price history."""

    history_price_currency_var_monthly: dict = None
    """dict: Monthly price history in base currency."""

    market_id_information: dict = None
    """dict: Additional market identifier information."""

    def __init__(self, security_id, lazy: bool = False):
        self.security_id = security_id
        # Defer enabling lazy loading until all initialization is complete.
        # This prevents ``__getattribute__`` from accessing ``__tasks__`` before
        # it is defined during object construction.
        self._lazy = False
        self.__qm__ = query_manager()
        self.__req_h__ = request_headers()

        if not security_id:
            raise ValueError("Security ID cannot be empty.")

        self.security_metadata = get_metadata(self.__qm__, self.security_id)
        self.security_type = self.security_metadata.get("securityType", None)

        if self.security_type is None:
            raise ValueError("Security type not found in metadata.")

        if self.security_type != "ST":
            raise ValueError("Incompatible security type.")

        self.queries_urls = [
            {
                "name": q["name"],
                "url": q["url"].replace("<STOCK_ID>", self.security_metadata["secId"]),
            }
            for q in stock_queries.get_queries()
        ]

        self.__tasks__ = {item["name"]: item["url"] for item in self.queries_urls}
        # Now that tasks are ready, store the requested lazy flag.
        self._lazy = lazy

        if not self._lazy:
            result = run_async(queries(self.__tasks__, headers=self.__req_h__))
            for k, v in result.items():
                setattr(self, k, v)
        else:
            for k in self.__tasks__:
                setattr(self, k, None)


@dataclass
class Fund(LazyFetchClass):
    disclosure_flag: dict = None
    """dict: Regulatory disclosure flags for the fund."""

    distribution_annual: dict = None
    """dict: Annual distribution data."""

    distribution_latest: dict = None
    """dict: Most recent distribution information."""

    esg_risk: dict = None
    """dict: ESG risk metrics."""

    esg_product_involvement: dict = None
    """dict: ESG product involvement details."""

    factor_exposure_profile: dict = None
    """dict: Factor exposure profile."""

    investment_strategy: dict = None
    """dict: Morningstar investment strategy commentary."""

    fixed_income_credit_quality_by_region: dict = None
    """dict: Fixed-income credit quality by region."""

    fixed_income_credit_quality_by_sector: dict = None
    """dict: Fixed-income credit quality by sector."""

    fixed_income_duration_by_credit_quality: dict = None
    """dict: Duration buckets by credit quality."""

    fixed_income_duration_by_region: dict = None
    """dict: Duration buckets by region."""

    fixed_income_duration_by_sector: dict = None
    """dict: Duration buckets by sector."""

    fixed_income_yield_to_worst_by_credit_quality: dict = None
    """dict: Yield to worst by credit quality."""

    fixed_income_yield_to_worst_by_region: dict = None
    """dict: Yield to worst by region."""

    fixed_income_yield_to_worst_by_sector: dict = None
    """dict: Yield to worst by sector."""

    parent_fund_flow: dict = None
    """dict: Fund flow graph data for the parent."""

    parent_medalist_rating_summary: dict = None
    """dict: Medalist rating summary for the parent."""

    parent_medalist_rating_top_funds: dict = None
    """dict: Top funds by medalist rating."""

    parent_medalist_rating_top_funds_up_down: dict = None
    """dict: Medalist rating flows for top funds."""

    parent_star_rating_fund_asc: dict = None
    """dict: Parent star ratings ascending."""

    parent_star_rating_fund_desc: dict = None
    """dict: Parent star ratings descending."""

    parent_star_rating_summary: dict = None
    """dict: Summary of parent star ratings."""

    parent_summary: dict = None
    """dict: Summary information about the parent fund."""

    people: dict = None
    """dict: Key personnel data."""

    market_volatility_measure_10y: dict = None
    """dict: Ten-year market volatility measures."""

    market_volatility_measure_3y: dict = None
    """dict: Three-year market volatility measures."""

    market_volatility_measure_5y: dict = None
    """dict: Five-year market volatility measures."""

    risk_return_scatterplot: dict = None
    """dict: Risk/return scatter plot data."""

    risk_return_summary: dict = None
    """dict: Risk/return summary metrics."""

    risk_score: dict = None
    """dict: Risk score metrics."""

    risk_volatility: dict = None
    """dict: Volatility measures used for risk analysis."""

    performance_annual_return_table: dict = None
    """dict: Annual return table."""

    performance_10k_growth: dict = None
    """dict: Growth of 10k performance data."""

    portfolio_credit_quality: dict = None
    """dict: Portfolio credit quality breakdown."""

    portfolio_holdings: dict = None
    """dict: Portfolio holdings data."""

    portfolio_regional_sector_exposure: dict = None
    """dict: Regional sector exposure data."""

    portfolio_regional_and_country_exposure: dict = None
    """dict: Regional and country exposure data."""

    portfolio_sector_exposure: dict = None
    """dict: Sector exposure using v2 endpoint."""

    price_cost_projection: dict = None
    """dict: Cost projection over time."""

    price_fee_level: dict = None
    """dict: Fee level classification."""

    price_investment_fee: dict = None
    """dict: Investment fee details."""

    price_other_fee: dict = None
    """dict: Other fee information."""

    price_overview: dict = None
    """dict: Price overview data."""

    process_asset_allocation: dict = None
    """dict: Asset allocation breakdown."""

    process_coupon_range: dict = None
    """dict: Coupon range distribution."""

    process_equity_style_box_history: dict = None
    """dict: Equity style box history."""

    process_financial_metrics: dict = None
    """dict: Key financial metrics."""

    process_fixed_income_style: dict = None
    """dict: Fixed income style information."""

    process_fixed_income_style_box_history: dict = None
    """dict: Fixed income style box history."""

    process_market_capitalization: dict = None
    """dict: Market capitalization breakdown."""

    process_maturity_schedule: dict = None
    """dict: Maturity schedule information."""

    process_ownership_zone: dict = None
    """dict: Ownership zone statistics."""

    process_stock_style: dict = None
    """dict: Stock style metrics (v2)."""

    process_weighting: dict = None
    """dict: Portfolio weighting data."""

    quote_overview: dict = None
    """dict: Investment overview quote data."""

    security_metadata: dict = None
    """dict: Metadata for the fund."""

    strategy_preview: dict = None
    """dict: Strategy preview details."""

    history_dividend_monthly: dict = None
    """dict: Monthly dividend history."""

    history_nav_total_return_post_tax_monthly: dict = None
    """dict: Monthly NAV total return after tax."""

    history_ohlcv_monthly: dict = None
    """dict: Monthly OHLCV price history."""

    history_post_tax_daily: dict = None
    """dict: Daily post-tax return history."""

    history_nav_total_return_daily: dict = None
    """dict: Daily NAV total return history."""

    history_nav_total_return_daily_recent: dict = None
    """dict: Recent daily NAV total return history."""

    history_nav_total_return_monthly: dict = None
    """dict: Monthly NAV total return history."""

    market_id_information: dict = None
    """dict: Additional market identifier information."""

    def __init__(self, security_id, lazy: bool = False):
        self.security_id = security_id
        # Defer enabling lazy loading until tasks are available. Otherwise
        # ``__getattribute__`` may fail when it tries to access ``__tasks__``
        # during initialization.
        self._lazy = False
        self.__qm__ = query_manager()
        self.__req_h__ = request_headers()

        if not security_id:
            raise ValueError("Security ID cannot be empty.")

        self.security_metadata = get_metadata(self.__qm__, self.security_id)
        self.security_type = self.security_metadata.get("securityType", None)

        if self.security_type is None:
            raise ValueError("Security type not found in metadata.")

        if self.security_type != "FO":
            raise ValueError("Incompatible security type.")

        self.queries_urls = [
            {
                "name": q["name"],
                "url": q["url"].replace("<FUND_ID>", self.security_metadata["secId"]),
            }
            for q in fund_queries.get_queries()
        ]

        self.__tasks__ = {item["name"]: item["url"] for item in self.queries_urls}
        # Now that tasks are initialized, apply the requested lazy flag
        self._lazy = lazy

        if not self._lazy:
            result = run_async(queries(self.__tasks__, headers=self.__req_h__))
            for k, v in result.items():
                setattr(self, k, v)
        else:
            for k in self.__tasks__:
                setattr(self, k, None)


__all__ = ["ETF", "Stock", "Fund"]
