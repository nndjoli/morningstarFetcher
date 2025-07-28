# MorningstarFetcher ETF Class Documentation:

**Usage Note & License**  
This library is intended for personal and educational use only. It is not affiliated with or endorsed by Morningstar. I do not encourage or condone scraping or any activity that violates Morningstar’s Terms of Service. Refer to the [MIT License](../LICENSE) in this repository for warranty and liability information.

Security IDs for ETFs can be retrieved via the [Screener](screener.md). Related documentation: [Stock](stock.md) and [Fund](fund.md).

```python
import morningstarFetcher
from pprint import pprint

etf = morningstarFetcher.ETF("0P00015WWF")  # Initialize ETF with a security ID;

portfolio_holdings = etf.portfolio_holdings  # ETF Portfolio Holdings;
pprint(portfolio_holdings)

financial_metrics = etf.process_financial_metrics  # Financial Metrics Information;
pprint(financial_metrics)
```

| Attribute | Description |
|-----------|-------------|
| `disclosure_flag` | dict: Regulatory disclosure flags for the ETF. |
| `distribution_annual` | dict: Annual distribution data in base currency. |
| `distribution_latest` | dict: Most recent distribution details. |
| `esg_risk` | dict: ESG risk metrics. |
| `esg_product_involvement` | dict: ESG product involvement breakdown. |
| `factor_exposure_profile` | dict: Factor exposure profile. |
| `investment_strategy` | dict: Morningstar investment strategy commentary. |
| `fixed_income_exposure` | dict: Fixed-income exposure details by region and sector. |
| `parent_fund_flow` | dict: Parent fund flow graph data. |
| `parent_medalist_rating_summary` | dict: Medalist rating summary for the parent fund. |
| `parent_medalist_rating_top_funds` | dict: Top funds ranked by medalist rating. |
| `parent_medalist_rating_top_funds_up_down` | dict: Medalist rating flows up/down for top funds. |
| `parent_fund_star_ratings_asc` | dict: Parent fund star ratings (ascending). |
| `parent_fund_star_ratings_desc` | dict: Parent fund star ratings (descending). |
| `parent_fund_overall_star_rating` | dict: Overall parent fund star rating. |
| `parent_fund_summary` | dict: Summary information about the parent fund. |
| `market_volatility_measure_10y` | dict: Ten-year market volatility measures. |
| `market_volatility_measure_3y` | dict: Three-year market volatility measures. |
| `market_volatility_measure_5y` | dict: Five-year market volatility measures. |
| `risk_return_scatterplot` | dict: Data for the risk/return scatter plot. |
| `risk_return_summary` | dict: Summary metrics of risk versus return. |
| `risk_score` | dict: Risk score values. |
| `risk_volatility` | dict: Volatility measures used for risk analysis. |
| `performance_table` | dict: Performance table of annual returns. |
| `performance_10k_growth` | dict: Growth of 10k and related performance data. |
| `portfolio_holdings` | dict: Portfolio holdings details. |
| `portfolio_regional_sector_exposure` | dict: Regional sector exposure breakdown. |
| `portfolio_regional_sector_include_countries` | dict: Regional and country sector exposures. |
| `portfolio_sector_exposure` | dict: Sector exposure using v2 endpoint. |
| `price_cost_projection` | dict: Projected costs over time. |
| `price_fee_level` | dict: Fee level classification. |
| `price` | dict: Latest price information. |
| `process_asset_allocation` | dict: Asset allocation data. |
| `process_equity_style_box_history` | dict: Historical equity style box positions. |
| `process_financial_metrics` | dict: Key financial metrics. |
| `process_market_capitalization` | dict: Market capitalization breakdown. |
| `process_ownership_zone` | dict: Ownership zone statistics. |
| `process_stock_style` | dict: Stock style information. |
| `process_weighting` | dict: Portfolio weighting by style. |
| `quote_mini_chart_realtime_data` | dict: Real-time mini chart price data. |
| `quote_investment_overview` | dict: Investment overview quote data. |
| `quote` | dict: Full quote information. |
| `history_dividend_monthly` | dict: Monthly dividend history. |
| `history_market_total_return_daily` | dict: Daily market total return history. |
| `history_price_monthly` | dict: Monthly price history. |
| `history_premium_discount_monthly` | dict: Monthly premium/discount history. |
| `history_price_daily` | dict: Daily price history. |
| `market_id_information` | dict: Additional market identifier information. |

Outputs:

```python
ETF Portfolio Holdings:
{'assetType': 'ALLOCATION',
 'baseCurrencyId': 'EUR',
 'boldHoldingPage': {'holdingList': [],
                     'numberOfAllHolding': 0,
                     'numberOfCurPageHolding': 0,
                     'pageNumber': 1,
                     'pageSize': 10000,
                     'previousPeriodsDate': None,
                     'totalPage': 0},
 'domicileCountryId': 'IRL',
 'equityHoldingPage': {'holdingList': [],
                       'numberOfAllHolding': 0,
                       'numberOfCurPageHolding': 0,
                       'pageNumber': 1,
                       'pageSize': 10000,
                       'previousPeriodsDate': None,
                       'totalPage': 0},
 'holdingActiveShare': {'activeShareDate': None,
                        'activeShareValue': None,
                        'etfBenchmarkProxyName': None,
                        'primaryProspectusBenchmark': 'Solactive Natural Gas '
                                                      'Com Fut SL TR EUR'},
 'holdingSummary': {'LastTurnoverDate': None,
                    'averageTurnoverRatio': None,
                    'equityNumberOfHolding': 0,
                    'fixedIncomeNumberOfHolding': 0,
                    'lastTurnover': None,
                    'numberOfHolding': 1,
                    'numberOfOtherHolding': 1,
                    'portfolioDate': '2021-08-31T05:00:00.000',
                    'secId': '0P00015WWF',
                    'topHoldingWeighting': 100.0,
                    'womenDirectors': None,
                    'womenExecutives': None},
 'masterPortfolioId': '2639528',
 'noPremiumChinaFund': False,
 'numberOfBondHolding': 0,
 'numberOfBondHoldingPer': 0.0,
 'numberOfBondHoldingShort': 0,
 'numberOfEquityHolding': 0,
 'numberOfEquityHoldingPer': 0.0,
 'numberOfEquityHoldingShort': 0,
 'numberOfHolding': 1,
 'numberOfHoldingShort': 0,
 'numberOfOtherHolding': 1,
 'numberOfOtherHoldingPer': 100.0,
 'numberOfOtherHoldingShort': 0,
 'otherHoldingPage': {'holdingList': [{'analystRating': '_PO_',
                                       'assessment': None,
                                       'bestRatingType': None,
                                       'country': 'United States',
                                       'coupon': None,
                                       'currency': None,
                                       'currencyName': None,
                                       'cusip': None,
                                       'domicileCountryId': None,
                                       'ePUsedForOverallRating': 0,
                                       'economicMoat': None,
                                       'epUsedFor1YearReturn': 0,
                                       'esgAsOfDate': None,
                                       'firstBoughtDate': None,
                                       'forwardPERatio': None,
                                       'holdingTrend': None,
                                       'holdingType': 'Other',
                                       'holdingTypeId': 'ST',
                                       'isMomentumFilterFlag': None,
                                       'isin': None,
                                       'lastTurnoverRatio': None,
                                       'localCurrencyCode': None,
                                       'managementExpenseRatio': None,
                                       'marketValue': 21972037.0,
                                       'maturityDate': None,
                                       'medalistRating': None,
                                       'medalistRatingLabel': None,
                                       'morningstarCategory': None,
                                       'morningstarRating': None,
                                       'numberOfShare': None,
                                       'oneYearReturn': None,
                                       'originalMarketValue': 21972037.24,
                                       'overallRatingPublishDateUtc': None,
                                       'performanceId': None,
                                       'primarySectorName': None,
                                       'prospectusNetExpenseRatio': None,
                                       'qualRating': None,
                                       'quantRating': None,
                                       'secId': None,
                                       'secondarySectorId': None,
                                       'secondarySectorName': None,
                                       'sector': None,
                                       'sectorCode': None,
                                       'securityName': 'TRS Solactive Natural '
                                                       'Gas Com Fut SL TR EUR',
                                       'securityType': None,
                                       'shareChange': None,
                                       'stockRating': None,
                                       'superSectorName': None,
                                       'susEsgRiskCategory': None,
                                       'susEsgRiskGlobes': None,
                                       'susEsgRiskScore': None,
                                       'ticker': None,
                                       'totalAssets': None,
                                       'totalAssetsMagnitude': None,
                                       'totalReturn1Year': None,
                                       'ttmYield': None,
                                       'weighting': 100.0}],
                      'numberOfAllHolding': 1,
                      'numberOfCurPageHolding': 1,
                      'pageNumber': 1,
                      'pageSize': 10000,
                      'previousPeriodsDate': None,
                      'totalPage': 1},
 'portfolioLastestDateFooter': '2021-08-31T05:00:00.000',
 'portfolioSuppression': '0',
 'secId': '0P00015WWF',
 'topNCount': 0,
 'userType': 'Free'}

Financial Metrics Information:
{'category': {'cashReturn': '_PO_',
              'debtToCapital': '_PO_',
              'financialHealthGradeType': '_PO_',
              'freeCashFlowYield': '_PO_',
              'growthGradeType': '_PO_',
              'masterPortfolioId': '674980',
              'narrowMoatPercentage': '_PO_',
              'noMoatPercentage': '_PO_',
              'portfolioDate': '2025-06-30T05:00:00.000',
              'profitabilityGradeType': '_PO_',
              'roic': '_PO_',
              'securityName': 'Trading - Leveraged/Inverse Commodities',
              'wideMoatPercentage': '_PO_'},
 'fund': {'cashReturn': '_PO_',
          'debtToCapital': '_PO_',
          'financialHealthGradeType': '_PO_',
          'freeCashFlowYield': '_PO_',
          'growthGradeType': '_PO_',
          'masterPortfolioId': '2639528',
          'narrowMoatPercentage': '_PO_',
          'noMoatPercentage': '_PO_',
          'portfolioDate': '2021-08-31T05:00:00.000',
          'profitabilityGradeType': '_PO_',
          'roic': '_PO_',
          'securityName': 'WisdomTree Natural Gas 3x Daily Lvrgd',
          'wideMoatPercentage': '_PO_'},
 'index': {'cashReturn': '_PO_',
           'debtToCapital': '_PO_',
           'financialHealthGradeType': '_PO_',
           'freeCashFlowYield': '_PO_',
           'growthGradeType': '_PO_',
           'masterPortfolioId': None,
           'narrowMoatPercentage': '_PO_',
           'noMoatPercentage': '_PO_',
           'portfolioDate': None,
           'profitabilityGradeType': '_PO_',
           'roic': '_PO_',
           'securityName': None,
           'wideMoatPercentage': '_PO_'},
 'userType': 'Free'}
```
