<h1>MorningstarFetcher</h1>

<div align="justify">
<b>MorningstarFetcher</b> is a Python package designed to interact with Morningstar’s public endpoints, simplifying access to financial data across various asset types (stocks, ETFs, mutual funds). It provides an interface for running market screeners and retrieving detailed information on specific securities. Its main goal is to streamline data retrieval for <b>asset management</b>—for example, to analyze portfolios, compare funds, or monitor risk and performance metrics.</div>
<hr>

<p align="justify"><h3>Table of Contents</h3></p>
<ul>
  <li><a href="#features">Features</a></li>
  <li><a href="#installation">Installation</a></li>
  <li><a href="#documentation">Documentation</a></li>
  <li><a href="#screener">Screener Class Overview</a></li>
  <li><a href="#asset-classes">Asset Classes Overview</a></li>
  <li><a href="#example">Example: Fetching and Analyzing Mutual Funds in France</a></li>
  <li><a href="#usage-note">Usage Note & License</a></li>
</ul>
<hr>

<p align="justify"><h3 id="features">Features</h3></p>

<div align="justify"  >
<ul>
  <li><b>Asynchronous Screener:</b> Query Morningstar’s screener to filter and list securities by market, investment type, etc.</li>
  <li><b>Asset Classes:</b> Dedicated classes (<code>ETF</code>, <code>Stock</code>, <code>Fund</code>) that automatically fetch and expose data attributes.</li>
  <li><b>Pandas Integration:</b> Screener results are returned as <code>pandas.DataFrame</code> for seamless data analysis.</li>
</ul>
</div>
<hr>



<p align="justify"><h3 id="installation">Installation</h3></p>

Pypi: <a href="https://pypi.org/project/morningstarFetcher/">https://pypi.org/project/morningstarFetcher/</a>
```bash
pip install morningstarFetcher
```
<hr>
<p align="justify"><h3 id="documentation">Documentation</h3></p>

<div align="justify">

<b>Detailed attribute listings and extended examples</b> are available in the <code>docs/</code> directory:

<ul>
  <li><a href="docs//screener.md">Screener Documentation</a></li>
  <li><a href="docs//stock.md">Stock Documentation</a></li>
  <li><a href="docs//fund.md">Fund Documentation</a></li>
  <li><a href="docs//etf.md">ETF Documentation</a></li>
</ul>

</div>
<hr>

<h3 id="screener">Screener Class Overview</h3>
<div align="justify">
The <code>Screener</code> class enables you to access Morningstar’s global screener, allowing you to filter and list securities by investment universe and geographic market. Supported universes include <code>"stocks"</code>, <code>"etfs"</code>, and <code>"mutual_funds"</code>. Use <code>screener.get()</code> with your chosen type to retrieve results for that universe. The class provides available markets via the <code>markets</code> attribute and country codes via <code>country_codes</code>, making it easy to target specific regions. Results from <code>get()</code> are returned as a <code>pandas.DataFrame</code> with columns such as <code>securityID</code>, <code>name</code>, and <code>isin</code>. You can further refine your search using custom filters based on fields available for each investment type. To see all filterable fields, access the <code>{your_investment_type}_fields</code> attribute. For full details, refer to the <a href="docs//screener.md">Screener documentation</a>.
</div>

<h4>Instantiation Example</h4>

```python
from morningstarFetcher import Screener

# Initialize the screener and inspect available markets
screener = Screener()
print("Available markets:", screener.markets)
print("Country codes:", screener.country_codes.keys())

# Fetch the first page of ETFs on the French market
results_df = screener.get("etfs", "fr")
print(results_df.head(5))  # DataFrame with securityID, name, isin, etc.

# Extract the first securityID
default_id = results_df.iloc[0]["securityID"]
print("First French ETF securityID:", default_id)
```
<div align="justify">
The returned DataFrame contains one row per security, each with a unique <code>securityID</code>. You can use this identifier with the <code>ETF</code>, <code>Stock</code>, or <code>Fund</code> classes to retrieve comprehensive details and attributes for that security.
</div>
<hr>

<h3 id="asset-classes">Asset Classes Overview:</h3>
<div align="justify">
The <b>ETF</b>, <b>Fund</b>, and <b>Stock</b> classes each represent a specific asset type and automatically retrieve relevant data from Morningstar when instantiated with a <code>securityID</code>. These classes provide direct access to key attributes such as price, performance, portfolio holdings, fund managers, insider transactions, and financial statements, depending on the asset type. Each class is designed for intuitive exploration of available data fields and methods. For comprehensive attribute and method documentation, see the <a href="docs/">documentation</a>.
</div>

<h4>Instantiation Example:</h4>

```python
from morningstarFetcher import ETF, Fund, Stock

etf_id   = "your_etf_id"
fund_id  = "your_fund_id"
stock_id = "your_stock_id"

etf   = ETF(etf_id)
fund  = Fund(fund_id)
stock = Stock(stock_id)

print("ETF price info:", etf.price)
print("Fund managers:", fund.people)
print("Stock valuation metrics:", stock.valuation)
```

Each object automatically retrieves all available fields for the given `securityID`.
<hr>

<h3 id="example">Example: Fetching and Analyzing Mutual Funds in France</h3>

<div align="justify">
<p>The following example demonstrates how to use the library to retrieve and analyze fund data for mutual funds. In this example we will focus on mutual funds domiciled in France with specific performance metrics. For this, we will use the <code>Screener</code> class to filter funds based on their 5-year total return and alpha, and then retrieve detailed portfolio holdings for each fund.</p>

<p>First we will set up the screener with the desired filters, then fetch the top mutual funds in France based on these filters.</p>


```python
import morningstarFetcher as mf
from pprint import pprint

screener = mf.Screener() # Initialize the screener

filters = [
  ["totalReturn[5y]", ">", "20"], # 5 year total return > 20%
  ["alpha[5yMonthly]", ">", "1"], # 5 year monthly alpha > 1
  ["domicile", "=", "FRA"] # Domicile in France
  ]
```
<b>Note:</b> The filters can be adjusted based on your specific requirements. The above filters are just examples to demonstrate the functionality. You can apply filter to any field included in the <code>{investment_type}_fields</code> attribute of the `Screener` class.

We then proceed to fetch the mutual funds using these filters and extract their security IDs to create `Fund` objects.

```python
french_mkt_funds_df = screener.get("mutual_funds", "fr", sort_by="totalReturn[5y]:desc", pages=1, filters=filters) # Fetch top mutual funds in France based on previous filters
french_mkt_funds_ids = french_mkt_funds_df["securityID"].tolist() # Extract security IDs of the funds
french_mkt_funds = [mf.Fund(sec_id, lazy=True) for sec_id in french_mkt_funds_ids] # Create Fund objects for each security ID
```
The `french_mkt_funds_df` DataFrame has more than 230 columns, including detailed performance metrics, risk assessments, and other valuable information about each fund. You can explore the `Screener` class documentation or its `{investment_type}_fields` attribute to see all available fields.

Next, we will iterate through each fund to extract its portfolio holdings and summarize the data. We will create a dictionary to hold the portfolio data for each fund, including its holdings summary and detailed holdings.

```python
french_market_funds_portfolios = {} # Dictionary to hold fund portfolios

for fund in french_mkt_funds:
    
    fund_id = fund.security_metadata['securityID'] if 'securityID' in fund.security_metadata else fund.security_metadata['secId']
    fund_isin = fund.security_metadata['isin']
    fund_name = fund.security_metadata['name']
    
    fund_holdings_summary = fund.portfolio_holdings.get('holdingSummary', {}) # Summary of holdings
    
    fund_equity_holdings = fund.portfolio_holdings.get('equityHoldingPage', {}).get('holdingList', []) # Raw list of equity holdings
    fund_bond_holdings = fund.portfolio_holdings.get('boldHoldingPage', {}).get('holdingList', []) # Raw list of bond holdings
    fund_other_holdings = fund.portfolio_holdings.get('otherHoldingPage', {}).get('holdingList', []) # Raw list of other holdings

    fund_holdings = {
        
        "equity": [
            {
                "id": security.get("securityID", None) or security.get("secId", None),
                "isin": security.get("isin", None),
                "name": security.get("securityName", None),
                "sector": security.get("sector", None),
                "country": security.get("country", None),
                "weighting": security.get("weighting", None),
                "firstBoughtDate": security.get("firstBoughtDate", None),
            } for security in fund_equity_holdings  # "Cleaned" List of equity holdings
        ],
        "bonds": [
            {
                "id": security.get("securityID", None) or security.get("secId", None),
                "isin": security.get("isin", None),
                "name": security.get("securityName", None),
                "sector": security.get("sector", None),
                "country": security.get("country", None),
                "weighting": security.get("weighting", None),
                "firstBoughtDate": security.get("firstBoughtDate", None),
            } for security in fund_bond_holdings # "Cleaned" List of bond holdings
        ],
        "other": [
            {
                "id": security.get("securityID", None) or security.get("secId", None),
                "isin": security.get("isin", None),
                "name": security.get("securityName", None),
                "sector": security.get("superSectorName", None),
                "country": security.get("country", None),
                "weighting": security.get("weighting", None),
                "firstBoughtDate": security.get("firstBoughtDate", None),
            } for security in fund_other_holdings # "Cleaned" List of other holdings
        ]
    } # Consolidated holdings data
    
    french_market_funds_portfolios[fund_id] = {
        'name': fund_name,
        'isin': fund_isin,
        'holdings_summary': fund_holdings_summary,
        'holdings': fund_holdings
    } # Store the portfolio data

```
Now that we have the portfolio data for each fund, we can analyze and print the holdings summary and detailed holdings for a specific fund. 

```python
id = french_mkt_funds_ids[0] # Example: Use the first fund's ID to retrieve its portfolio data
data = french_market_funds_portfolios[id] # Retrieve the portfolio data for the selected fund

holdings_summary = data['holdings_summary']
print("Holdings Summary:", end=f'\n{"-"*80}\n')
pprint(holdings_summary, compact=True, sort_dicts=False) # Print holdings summary
print()

equity_holdings = pd.DataFrame(data['holdings']['equity']).sort_values(by='weighting', ascending=False)
print("Equity Holdings:", end=f'\n{"-"*80}\n')
pprint(equity_holdings, compact=False, sort_dicts=False) # Print equity holdings

other_holdings = pd.DataFrame(data['holdings']['other']).sort_values(by='weighting', ascending=False)
print("Other Holdings:", end=f'\n{"-"*80}\n')
pprint(other_holdings, compact=False, sort_dicts=False) # Print other holdings
print()

equity_weight = equity_holdings['weighting'].sum()
print(f"Equity Weight: {equity_weight}") # Check total equity weight

other_weight = other_holdings['weighting'].sum()
print(f"Other Weight: {other_weight}") # Check total other weight

total = equity_weight + other_weight
print(f"Total Weight: {total}") # Check total weight of all holdings
```

<p><u>The output is as follows:</u></p>

```
Holdings Summary:
------------------------------------------------------------------------------------------------------------------------------------------------------
'portfolioDate': '2025-05-31T05:00:00.000',
'topHoldingWeighting': 47.54024,
'equityNumberOfHolding': 35,
'fixedIncomeNumberOfHolding': 0,
'numberOfHolding': 36,
'numberOfOtherHolding': 1,
'lastTurnover': -51.3,
'LastTurnoverDate': '2011-06-30T05:00:00.000',
'secId': 'F000010ELX',
'averageTurnoverRatio': None,
'womenDirectors': 42.84,
'womenExecutives': 22.09

Equity Holdings:
------------------------------------------------------------------------------------------------------------------------------------------------------
            id          isin                                         name                  sector         country  weighting          firstBoughtDate  
0   0P00009QNO  DE0008404005                                   Allianz SE      Financial Services         Germany    7.08596  2022-09-30T05:00:00.000  
1   0P0000A5JA  ES0113900J37                           Banco Santander SA      Financial Services           Spain    5.93349  2022-11-30T06:00:00.000  
2   0P0000A5GW  CH0011075394                    Zurich Insurance Group AG      Financial Services     Switzerland    5.26197  2022-06-30T05:00:00.000  
3   0P00009DOL  IT0005239360                                UniCredit SpA      Financial Services           Italy    4.78387  2024-12-31T06:00:00.000  
4   0P00009QR8  DE0008430026  Munchener Ruckversicherungs-Gesellschaft AG      Financial Services         Germany    4.66989  2021-05-31T05:00:00.000  
5   0P00009DL7  IT0000072618                              Intesa Sanpaolo      Financial Services           Italy    4.59693  2024-12-31T06:00:00.000  
6   0P00009WBE  FR0000120628                                       AXA SA      Financial Services          France    4.57784  2021-12-31T06:00:00.000  
7   0P00009QOT  DE0005810055                           Deutsche Boerse AG      Financial Services         Germany    3.72079  2022-06-30T05:00:00.000  
8   0P000090MW  GB00BM8PJY71                            NatWest Group PLC      Financial Services  United Kingdom    3.46696  2021-12-31T06:00:00.000  
9   0P0000TDIK  CH0126881561                                  Swiss Re AG      Financial Services     Switzerland    3.42261  2022-11-30T06:00:00.000  
10  0P00009QOR  DE0005140008                             Deutsche Bank AG      Financial Services         Germany    3.31545  2025-05-31T05:00:00.000  
11  0P00009WPY  FR0000130809                          Societe Generale SA      Financial Services          France    2.92195  2025-05-31T05:00:00.000  
12  0P00009DKL  IT0000062072                                     Generali      Financial Services           Italy    2.69185  2024-12-31T06:00:00.000  
13  0P0000AYAS  ES0140609019                                 CaixaBank SA      Financial Services           Spain    2.68746  2022-09-30T05:00:00.000  
14  0P0000A5RZ  ES0113211835           Banco Bilbao Vizcaya Argentaria SA      Financial Services           Spain    2.58784  2022-12-31T06:00:00.000  
15  0P0000A6NH  FI4000552500                            Sampo Oyj Class A      Financial Services         Finland    2.42717  2021-12-31T06:00:00.000  
16  0P000090RJ  GB00BPQY8M80                                    Aviva PLC      Financial Services  United Kingdom    2.30656  2022-11-30T06:00:00.000  
17  0P00009QQ2  DE0008402215          Hannover Rueck SE Registered Shares      Financial Services         Germany    2.18706  2023-06-30T05:00:00.000  
18  0P0000CG34  IE00BF0L3536                                AIB Group PLC      Financial Services         Ireland    2.17107  2022-12-31T06:00:00.000  
19  0P00013KYD  NL0010773842                                  NN Group NV      Financial Services     Netherlands    2.14498  2025-04-30T05:00:00.000  
20  0P0000C2OL  IE00BD1RP616                    Bank of Ireland Group PLC      Financial Services         Ireland    2.02803  2022-12-31T06:00:00.000  
21  0P00009DM4  IT0000062957                               Mediobanca SpA      Financial Services           Italy    1.97023  2025-05-31T05:00:00.000  
22  0P00013DKO  NL0006294274                                  Euronext NV      Financial Services     Netherlands    1.95561  2024-06-30T05:00:00.000  
23  0P00007NVV  GB00B02J6398                            Admiral Group PLC      Financial Services  United Kingdom    1.93806  2024-03-31T05:00:00.000  
24  0P000184F7  NL0011872643                             ASR Nederland NV      Financial Services     Netherlands    1.89784  2025-04-30T05:00:00.000  
25  0P00016X4J  IT0003796171                           Poste Italiane SpA           Industrials           Italy    1.89779  2023-04-30T05:00:00.000  
26  0P0000A5MB  BE0974264930                                 Ageas SA/ NV      Financial Services         Belgium    1.85755  2021-12-31T06:00:00.000  
27  0P0000X4GY  DE000TLX1005                                    Talanx AG      Financial Services         Germany    1.81255  2023-06-30T05:00:00.000  
28  0P0000A5RI  DK0060636678                                      Tryg AS      Financial Services         Denmark    1.80850  2021-12-31T06:00:00.000  
29  0P00009DON  IT0004810054                     Unipol Assicurazioni SpA      Financial Services           Italy    1.77975  2024-12-31T06:00:00.000  
30  0P00007OS9  GB0007099541                               Prudential PLC      Financial Services  United Kingdom    1.27519  2025-04-30T05:00:00.000  
31  0P0000A5MC  BE0003797140                  Groupe Bruxelles Lambert SA      Financial Services         Belgium    1.14945  2025-04-30T05:00:00.000  
32  0P0000RXLJ  NO0010582521                    Gjensidige Forsikring ASA      Financial Services          Norway    0.91182  2025-04-30T05:00:00.000  
33  0P0000A63I  NL0011821202                                 ING Groep NV      Financial Services     Netherlands    0.87152  2025-05-31T05:00:00.000  
34  0P0000A6PJ  BMG0112X1056                                    Aegon Ltd      Financial Services     Netherlands    0.44186  2025-05-31T05:00:00.000  

Other Holdings:
------------------------------------------------------------------------------------------------------------------------------------------------------
            id          isin          name             sector         country         weighting          firstBoughtDate  
0  E0GBR00IH4  GB00B1YW4409  3i Group Ord        None     United Kingdom          3.44254                  None  

Equity Weight: 96.55745
Other Weight: 3.44254
Total Weight: 99.99999
---
```
</div>

<hr>
<h3 id="usage-note">Usage Note & License</h3>
This library is intended for personal and educational use only. It is not affiliated with or endorsed by Morningstar. I do not encourage or condone scraping or any activity that violates Morningstar’s Terms of Service. Refer to the <a href="LICENSE">MIT License</a> in this repository for warranty and liability information.
