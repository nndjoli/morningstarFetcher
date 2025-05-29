<h1>msfunds</h1> 

- Interacts with the Morningstar API to retrieve fund-related data.
- Includes a screener to filter and identify funds based on specific criteria.

<h2>Requirements & Installation :</h2>

- Requirements: `ua_generator`, `httpx`, `pandas`, `beautifulsoup4`, `nest_asyncio`, `importlib_resources`.  
- Install using: `pip install msfunds` (https://pypi.org/project/msfunds/)
 


<h2>Example:</h2>

```python
import msfunds

# Initialize the screener function class
sc = msfunds.ScreenerFunction()
```
The screener function is accessible via: 

```python

# Call the screener function
df = sc.screener() 
```
Its parameters are:

```text
    CountryName (str): Target country name; defaults to 'France'.
    Keyword (str): Search term; defaults to empty.
    BrandingCompanyId: Branding company filter key.
    Fields (list): Fields to return; must include 'Name' and 'SecId'.
    AdministratorCompanyId: Administrator company filter key.
    CategoryId: Category filter key.
    GlobalCategoryId: Global category filter key.
    GlobalAssetClassId: Global asset class filter key.
    IMASectorID: IMA sector filter key.
    LargestRegion: Largest region filter key.
    LargestSector: Largest sector filter key.
    ShareClassTypeId: Share class type filter key.
    ManagementStyle: Management style filter key.
    distribution: Distribution filter key.
    FeeLevel: Fee level filter key or range.
    OngoingCharge: Ongoing charge filter key.
    CollectedSRRI: SRRI filter key.
    StarRatingM255: Star rating filter key.
    Medalist_RatingNumber: Medalist rating filter key.
    SustainabilityRank: Sustainability rank filter key.
    InvestorType: Investor type filter key.
    Expertise: Expertise filter key.
    ReturnProfile: Return profile filter key.
    Page (int): Page number; defaults to 1.
    sortOrder (str): Sort expression; defaults to 'LegalName asc'.
    PageSize (int): Results per page; defaults to 10000.
```

You can access valid values for a parameter by calling its associated class attribute. For example if you want to filter funds by `LargestSector` or `GlobalAssetClassId`:

```python
sc.largest_sector
>>> {
    'All': 'null',
    'Basic Materials': 'SB_BasicMaterials',
    'Communication Services': 'SB_CommunicationServices',
    'Consumer Cyclical': 'SB_ConsumerCyclical',
    'Consumer Defensive': 'SB_ConsumerDefensive',
    'Energy': 'SB_Energy',
    'Financial Services': 'SB_FinancialServices',
    'Healthcare': 'SB_Healthcare',
    'Industrials': 'SB_Industrials',
    'Real Estate': 'SB_RealEstate',
    'Technology': 'SB_Technology',
    'Utilities': 'SB_Utilities'
}
```
```python
sc.global_asset_class_ids
>>>{
    'All': 'null',
    'Allocation': '$BCG$ALLOC',
    'Alternative': '$BCG$ALTER',
    'Commodities': '$BCG$COMMO',
    'Convertibles': '$BCG$CONVT',
    'Equity': '$BCG$EQUTY',
    'Fixed Income': '$BCG$FXINC',
    'Miscellaneous': '$BCG$MISCL',
    'Money Market': '$BCG$MNMKT',
    'Property': '$BCG$PRPTY'
}
```
<strong>Note:</strong> Some company IDs might not be available in the dictionary returned by the attributes `BrandingCompanyId` and `AdministratorCompanyId`. If that is the case, please refer to the <a href="https://www.morningstar.com/">Morningstar</a> website.

```python
df = sc.screener(CountryName='France', Keyword='Tech', Fields=['GBRReturnM1', 'GBRReturnM3', 'GBRReturnM6'])
df = df.sort_values(by='GBRReturnM3', ascending=False)
df = df.head(10)
>>>
```
|     | Name                                  | SecId      | GBRReturnM1 | GBRReturnM3 | GBRReturnM6 |
|-----|---------------------------------------|------------|-------------|-------------|-------------|
| 390 | Sycomore Fund Sustainable Tech FC EUR | F0000161VH |       15.71 |       26.93 |       27.82 |
| 150 | EdR SICAV Tech for Tomorrow I USD     | F0000161R6 |        3.27 |       13.87 |       14.46 |
| 223 | Janus Henderson Glb Tech&Inno H2 HEUR | F00000QM3C |       12.15 |        6.69 |        3.72 |
| 226 | Janus Henderson Glb Tech&Inno I2 HEUR | F000000S5D |       12.09 |        6.50 |        3.37 |
| 219 | Janus Henderson Glb Tech&Inno A2 HEUR | F0GBR04J0E |       12.02 |        6.31 |        2.97 |
| 152 | EdR SICAV Tech for Tomorrow K EUR     | F000015EJW |       -4.72 |        6.14 |       13.75 |
| 151 | EdR SICAV Tech for Tomorrow J USD     | F0000161R5 |        5.80 |        5.71 |       -2.43 |
| 178 | Franklin Technology I Acc EUR H1      | F000015O4W |       12.97 |        5.33 |        1.15 |
| 186 | Franklin Technology W Acc EUR-H1      | F000010EYW |       13.00 |        5.31 |        1.12 |
| 356 | PrivilEdge Fidelity Tech SysH EUR RA  | F00000XHD7 |        1.79 |        5.08 |        8.06 |

You can then call the Fund class with the fund ID 
```python
fund_id = df.iloc[0]['SecId'] # Get the first fund ID
fund = msfunds.Fund(fund_id)  # Initialize the Fund object
```
Its attributes are: 
```text
- ESG: ESG data endpoints.
- ESGRisk: ESG risk data endpoints.
- FactorProfile: Factor profile data endpoints.
- MorningstarTake: Morningstar take data endpoints.
- MultiLevelFixedIncomeData: Multi-level fixed income data endpoints.
- ParentFund: Parent fund data endpoints.
- People: People-related data endpoints.
- Performance: Performance data endpoints.
- Portfolio: Portfolio data endpoints.
- Price: Price data endpoints.
- Process: Process data endpoints.
- Quote: Quote data endpoints.
- SecurityMetaData: Security metadata endpoints.
- StrategyPreview: Strategy preview data endpoints.
- TrailingReturn: Trailing return data endpoints.
```
Each attribute of the `Fund` class returns a dictionary containing attribute-name related datas. For example the Portfolio attribute returns dictionaries containing information on the fund portfolio composition.

```python
fund.Portfolio.keys()
>>>dict_keys(['HoldingData', 'HoldingPar', 'RegionalSector', 'V2'])

fund.Portfolio['HoldingPar'].keys()
>>>dict_keys(['masterPortfolioId', 'secId', 'baseCurrencyId', 'domicileCountryId',
 'numberOfHolding', 'numberOfEquityHolding', 'numberOfBondHolding', 'numberOfOtherHolding',
 'numberOfHoldingShort', 'numberOfEquityHoldingShort', 'numberOfBondHoldingShort',
 'numberOfOtherHoldingShort', 'topNCount', 'portfolioSuppression', 'assetType', 'holdingSummary',
 'holdingActiveShare', 'equityHoldingPage', 'boldHoldingPage', 'otherHoldingPage', 'userType',
 'portfolioLastestDateFooter', 'noPremiumChinaFund', 'numberOfEquityHoldingPer',
 'numberOfBondHoldingPer', 'numberOfOtherHoldingPer'])

# Display holdings summary:
fund.Portfolio['HoldingPar']['holdingSummary']
>>>{
    'portfolioDate': '2025-04-30T05:00:00.000',
    'topHoldingWeighting': 32.81196,
    'equityNumberOfHolding': 40,
    'fixedIncomeNumberOfHolding': 0,
    'numberOfHolding': 93,
    'numberOfOtherHolding': 53,
    'lastTurnover': None,
    'LastTurnoverDate': None,
    'secId': 'F0000161VH',
    'averageTurnoverRatio': None,
    'womenDirectors': 31.58,
    'womenExecutives': 19.63
}

# Display Equity holdings per sector
fund.Portfolio['V2']['EQUITY']['fundPortfolio'] 
>>>{
    'portfolioDate': '2025-04-30T05:00:00.000',
    'basicMaterials': 0.0,
    'consumerCyclical': 0.0,
    'financialServices': 0.0,
    'realEstate': 0.0,
    'communicationServices': 0.0,
    'energy': 0.0,
    'industrials': 1.0119,
    'technology': 96.82767,
    'consumerDefensive': 0.0,
    'healthcare': 2.16044,
    'utilities': 0.0
}

# Display Fixed-Income holdings per sector
fund.Portfolio['V2']['FIXEDINCOME']['fundPortfolio'] 
>>>{
    'portfolioDate': '2025-04-30T05:00:00.000',
    'government': 0.0,
    'municipal': 0.0,
    'corporate': 0.0,
    'securitized': 0.0,
    'cashAndEquivalents': 100.0,
    'derivative': 0.0
}


# Display top equity holdings
holdings = fund.Portfolio['HoldingPar']['equityHoldingPage']['holdingList'] 
holdings_df = pd.DataFrame(holdings)
holdings_df.columns
>>>Index(['securityName', 'secId', 'performanceId', 'holdingTypeId', 'weighting',
       'numberOfShare', 'marketValue', 'shareChange', 'country', 'ticker',
       'totalReturn1Year', 'forwardPERatio', 'stockRating', 'assessment',
       'economicMoat', 'sector', 'sectorCode', 'holdingTrend', 'holdingType',
       'isin', 'cusip', 'secondarySectorId', 'superSectorName',
       'primarySectorName', 'secondarySectorName', 'firstBoughtDate',
       'maturityDate', 'coupon', 'currency', 'localCurrencyCode',
       'prospectusNetExpenseRatio', 'oneYearReturn', 'morningstarRating',
       'ePUsedForOverallRating', 'analystRating', 'medalistRating',
       'medalistRatingLabel', 'overallRatingPublishDateUtc', 'totalAssets',
       'ttmYield', 'epUsedFor1YearReturn', 'morningstarCategory',
       'totalAssetsMagnitude', 'lastTurnoverRatio', 'susEsgRiskScore',
       'susEsgRiskGlobes', 'esgAsOfDate', 'susEsgRiskCategory',
       'managementExpenseRatio', 'qualRating', 'quantRating', 'bestRatingType',
       'securityType', 'domicileCountryId', 'currencyName',
       'originalMarketValue', 'isMomentumFilterFlag'],
      dtype='object')


cols = [
  'securityName','ticker',
  'sector', 'weighting',
  'firstBoughtDate', 'numberOfShare',
  'marketValue', 'totalReturn1Year',
  'forwardPERatio'
]

holdings_df = holdings_df[cols]
>>>
```
| securityName                              | ticker | sector     | weighting | firstBoughtDate         | numberOfShare | marketValue  | totalReturn1Year | forwardPERatio |
|:------------------------------------------|:--------|:-----------|----------:|:------------------------|--------------:|-------------:|-----------------:|---------------:|
| Taiwan Semiconductor Manufacturing Co Ltd | 2330    | Technology |      9.76 | 2020-11-30T06:00:00.000 |      1256539  |   31,381,808 |            12.89 |          16.78 |
| Microsoft Corp                            | MSFT    | Technology |      7.56 | 2020-11-30T06:00:00.000 |        69884  |   24,299,406 |             7.85 |          30.67 |
| NVIDIA Corp                               | NVDA    | Technology |      6.83 | 2023-02-28T06:00:00.000 |       229098  |   21,951,488 |            27.30 |          31.45 |
| Workday Inc Class A                       | WDAY    | Technology |      4.61 | 2024-05-31T05:00:00.000 |        68680  |   14,802,375 |             8.32 |          27.86 |
| Synopsys Inc                              | SNPS    | Technology |      4.20 | 2020-11-30T06:00:00.000 |        33388  |   13,481,791 |           -12.87 |          34.48 |
| ASML Holding NV                           | ASML    | Technology |      4.16 | 2020-11-30T06:00:00.000 |        22955  |   13,371,287 |           -23.80 |          27.47 |
| Adobe Inc                                 | ADBE    | Technology |      4.03 | 2025-02-28T06:00:00.000 |        39282  |   12,957,963 |           -13.11 |          20.24 |
| Broadcom Inc                              | AVGO    | Technology |      3.50 | 2023-08-31T05:00:00.000 |        66378  |   11,238,860 |            68.97 |          35.84 |


You can view an example of the results of most of the attributes by looking at the <a href="https://github.com/nndjoli/morningstar-funds-data-fetcher/blob/main/msfunds/Tests/fund_test.json">fund test file </a>.

Since the output data is raw, exporting it as a `.json` file can help you locate information related to a specific subject by using `CTRL+F` within the file.

```python

import json
import datetime as dt

fund_id = "your_fund_id"
fund_data = msfunds.Fund(fund_id)
fund_dict = fund_data.__dict__
filename = f"MSFundsData_{fund_id}_{str(dt.date.today())}.json"

with open(filename, "w", encoding="utf-8") as f:
    json.dump(fund_dict, f, indent=4)
```

<strong>Note:</strong> The `Fund` class relies on an authentication token generated by the Morningstar website. If too many requests are made (e.g., by repeatedly instantiating the `Fund` class), the token may fail to load, and you will need to wait before successfully accessing the data again.
