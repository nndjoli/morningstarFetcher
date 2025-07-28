# MorningstarFetcher Fund Class Documentation:

**Usage Note & License**  
This library is intended for personal and educational use only. It is not affiliated with or endorsed by Morningstar. I do not encourage or condone scraping or any activity that violates Morningstar’s Terms of Service. Refer to the [MIT License](../LICENSE) in this repository for warranty and liability information.

Use the [Screener](screener.md) to locate fund identifiers. For other asset types see [ETF](etf.md) and [Stock](stock.md).


```python
import morningstarFetcher
from pprint import pprint

fund = morningstarFetcher.Fund("0P00000JRR")  # Initialize Fund;

summary = fund.parent_summary  # Parent fund summary;
pprint(summary)

people = fund.people  # Key personnel;
pprint(people)
```

| Attribute | Description |
|-----------|-------------|
| `disclosure_flag` | dict: Regulatory disclosure flags for the fund. |
| `distribution_annual` | dict: Annual distribution data. |
| `distribution_latest` | dict: Most recent distribution information. |
| `esg_risk` | dict: ESG risk metrics. |
| `esg_product_involvement` | dict: ESG product involvement details. |
| `factor_exposure_profile` | dict: Factor exposure profile. |
| `investment_strategy` | dict: Morningstar investment strategy commentary. |
| `fixed_income_credit_quality_by_region` | dict: Fixed-income credit quality by region. |
| `fixed_income_credit_quality_by_sector` | dict: Fixed-income credit quality by sector. |
| `fixed_income_duration_by_credit_quality` | dict: Duration buckets by credit quality. |
| `fixed_income_duration_by_region` | dict: Duration buckets by region. |
| `fixed_income_duration_by_sector` | dict: Duration buckets by sector. |
| `fixed_income_yield_to_worst_by_credit_quality` | dict: Yield to worst by credit quality. |
| `fixed_income_yield_to_worst_by_region` | dict: Yield to worst by region. |
| `fixed_income_yield_to_worst_by_sector` | dict: Yield to worst by sector. |
| `parent_fund_flow` | dict: Fund flow graph data for the parent. |
| `parent_medalist_rating_summary` | dict: Medalist rating summary for the parent. |
| `parent_medalist_rating_top_funds` | dict: Top funds by medalist rating. |
| `parent_medalist_rating_top_funds_up_down` | dict: Medalist rating flows for top funds. |
| `parent_star_rating_fund_asc` | dict: Parent star ratings ascending. |
| `parent_star_rating_fund_desc` | dict: Parent star ratings descending. |
| `parent_star_rating_summary` | dict: Summary of parent star ratings. |
| `parent_summary` | dict: Summary information about the parent fund. |
| `people` | dict: Key personnel data. |
| `market_volatility_measure_10y` | dict: Ten-year market volatility measures. |
| `market_volatility_measure_3y` | dict: Three-year market volatility measures. |
| `market_volatility_measure_5y` | dict: Five-year market volatility measures. |
| `risk_return_scatterplot` | dict: Risk/return scatter plot data. |
| `risk_return_summary` | dict: Risk/return summary metrics. |
| `risk_score` | dict: Risk score metrics. |
| `risk_volatility` | dict: Volatility measures used for risk analysis. |
| `performance_annual_return_table` | dict: Annual return table. |
| `performance_10k_growth` | dict: Growth of 10k performance data. |
| `portfolio_credit_quality` | dict: Portfolio credit quality breakdown. |
| `portfolio_holdings` | dict: Portfolio holdings data. |
| `portfolio_regional_sector_exposure` | dict: Regional sector exposure data. |
| `portfolio_regional_and_country_exposure` | dict: Regional and country exposure data. |
| `portfolio_sector_exposure` | dict: Sector exposure using v2 endpoint. |
| `price_cost_projection` | dict: Cost projection over time. |
| `price_fee_level` | dict: Fee level classification. |
| `price_investment_fee` | dict: Investment fee details. |
| `price_other_fee` | dict: Other fee information. |
| `price_overview` | dict: Price overview data. |
| `process_asset_allocation` | dict: Asset allocation breakdown. |
| `process_coupon_range` | dict: Coupon range distribution. |
| `process_equity_style_box_history` | dict: Equity style box history. |
| `process_financial_metrics` | dict: Key financial metrics. |
| `process_fixed_income_style` | dict: Fixed income style information. |
| `process_fixed_income_style_box_history` | dict: Fixed income style box history. |
| `process_market_capitalization` | dict: Market capitalization breakdown. |
| `process_maturity_schedule` | dict: Maturity schedule information. |
| `process_ownership_zone` | dict: Ownership zone statistics. |
| `process_stock_style` | dict: Stock style metrics (v2). |
| `process_weighting` | dict: Portfolio weighting data. |
| `quote_overview` | dict: Investment overview quote data. |
| `security_metadata` | dict: Metadata for the fund. |
| `strategy_preview` | dict: Strategy preview details. |
| `history_dividend_monthly` | dict: Monthly dividend history. |
| `history_nav_total_return_post_tax_monthly` | dict: Monthly NAV total return after tax. |
| `history_ohlcv_monthly` | dict: Monthly OHLCV price history. |
| `history_post_tax_daily` | dict: Daily post-tax return history. |
| `history_nav_total_return_daily` | dict: Daily NAV total return history. |
| `history_nav_total_return_daily_recent` | dict: Recent daily NAV total return history. |
| `history_nav_total_return_monthly` | dict: Monthly NAV total return history. |
| `market_id_information` | dict: Additional market identifier information. |

Outputs:

