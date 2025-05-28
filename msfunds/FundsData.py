import ua_generator
import nest_asyncio

nest_asyncio.apply()
import asyncio
import httpx


def reqheaders():

    headers = {
        "User-Agent": ua_generator.generate(device="desktop", browser=("chrome", "edge")).text,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "referer": "https://www.morningstar.com/",
    }

    token_response = httpx.get("https://www.morningstar.com/funds/xnas/broix/chart", follow_redirects=True, timeout=120.0, headers=headers)

    if token_response.status_code != 200:
        raise Exception("Too many requests: Failed to retrieve token from Morningstar. Please try again later.")

    resp = token_response.text

    if resp.find("token") != -1:
        token_start = resp[resp.find("token") :]
        dx = token_start[7 : token_start.find("}") - 1]
    else:
        raise Exception("Authentication token not found in the response.")

    headers["authorization"] = f"Bearer {dx}"
    headers["apikey"] = "lstzFDEOhfFNMLikKa0am9mgEKLBl49T"

    return headers


async def query(client, url):
    try:
        response = await client.get(url)
        return response.json()

    except Exception as e:
        return {"Error": str(e), "URL": url}


async def queries(FundID: str):

    headers = reqheaders()

    async with httpx.AsyncClient() as client:

        # Auth-related headers
        client.headers.update(headers)

        TASKS = {
            # ESG Data:
            "GlobalAPI_ESG_CarbonMetrics": query(client, f"https://api-global.morningstar.com/sal-service/v1/fund/esg/carbonMetrics/{FundID}/data"),
            "GlobalAPI_ESG_V1": query(client, f"https://api-global.morningstar.com/sal-service/v1/fund/esg/v1/{FundID}/data"),
            # ESG Risk Data:
            "GlobalAPI_ESGRISK_blank": query(client, f"https://api-global.morningstar.com/sal-service/v1/fund/esgRisk/{FundID}/data"),
            # Factor Profile Data:
            "GlobalAPI_FACTORPROFILE": query(client, f"https://api-global.morningstar.com/sal-service/v1/fund/factorProfile/{FundID}/data"),
            # Morningstar Take Data:
            "GlobalAPI_MORNINGSTARTAKE_InvestmentStrategy": query(client, f"https://api-global.morningstar.com/sal-service/v1/fund/morningstarTake/investmentStrategy/{FundID}/data"),
            # Multi-Level Fixed Income Data:
            "GlobalAPI_MULTILEVELFIXEDINCOMEDATA": query(client, f"https://api-global.morningstar.com/sal-service/v1/fund/multiLevelFixedIncomeData/{FundID}/data"),
            # Parent Fund Data:
            "GlobalAPI_PARENT_GraphData": query(client, f"https://api-global.morningstar.com/sal-service/v1/fund/parent/graphData/{FundID}/data"),
            "GlobalAPI_PARENT_MedalistRating_TopFunds": query(client, f"https://api-global.morningstar.com/sal-service/v1/fund/parent/medalistRating/topfunds/{FundID}/data"),
            "GlobalAPI_PARENT_MedalistRating_TopFundsUpDown": query(client, f"https://api-global.morningstar.com/sal-service/v1/fund/parent/medalistRating/topfundsUpDown/{FundID}/data"),
            "GlobalAPI_PARENT_MedalistRating": query(client, f"https://api-global.morningstar.com/sal-service/v1/fund/parent/medalistRating/{FundID}/data"),
            "GlobalAPI_PARENT_ParentSummary": query(client, f"https://api-global.morningstar.com/sal-service/v1/fund/parent/parentSummary/{FundID}/data"),
            # People Data:
            "GlobalAPI_PEOPLE_ProxyVoting_Management": query(client, f"https://api-global.morningstar.com/sal-service/v1/fund/people/proxyVoting/management/{FundID}/data"),
            "GlobalAPI_PEOPLE_ProxyVoting_ShareHolder": query(client, f"https://api-global.morningstar.com/sal-service/v1/fund/people/proxyVoting/shareHolder/v1/{FundID}/data"),
            "GlobalAPI_PEOPLE": query(client, f"https://api-global.morningstar.com/sal-service/v1/fund/people/{FundID}/data"),
            # Performance Data:
            "GlobalAPI_PERFORMANCE_MarketVolatilityMeasure": query(client, f"https://api-global.morningstar.com/sal-service/v1/fund/performance/marketVolatilityMeasure/{FundID}/data"),
            "GlobalAPI_PERFORMANCE_RiskReturnScatterplot": query(client, f"https://api-global.morningstar.com/sal-service/v1/fund/performance/riskReturnScatterplot/{FundID}/data"),
            "GlobalAPI_PERFORMANCE_RiskReturnSummary": query(client, f"https://api-global.morningstar.com/sal-service/v1/fund/performance/riskReturnSummary/{FundID}/data"),
            "GlobalAPI_PERFORMANCE_RiskScore": query(client, f"https://api-global.morningstar.com/sal-service/v1/fund/performance/riskScore/{FundID}/data"),
            "GlobalAPI_PERFORMANCE_RiskVolatility": query(client, f"https://api-global.morningstar.com/sal-service/v1/fund/performance/riskVolatility/{FundID}/data"),
            "GlobalAPI_PERFORMANCE_Table": query(client, f"https://api-global.morningstar.com/sal-service/v1/fund/performance/table/{FundID}?secExchangeList=&limitAge=&hideYTD=false&languageId=en&locale=en&clientId=MDC&benchmarkId=mstarorcat&component=sal-mip-annual-return&version=4.63.0"),
            "GlobalAPI_PERFORMANCE_V5": query(client, f"https://api-global.morningstar.com/sal-service/v1/fund/performance/v5/{FundID}?secExchangeList=&limitAge=&hideYTD=false&languageId=en&locale=en&clientId=MDC&benchmarkId=mstarorcat&component=sal-mip-growth-10k&version=4.63.0"),
            # Portfolio Data:
            "GlobalAPI_PORTFOLIO_HoldingData": query(client, f"https://api-global.morningstar.com/sal-service/v1/fund/portfolio/holding/v2/{FundID}/data"),
            "GlobalAPI_PORTFOLIO_HoldingPar": query(client, f"https://api-global.morningstar.com/sal-service/v1/fund/portfolio/holding/v2/{FundID}/data?premiumNum=10000&freeNum=10000"),
            "GlobalAPI_PORTFOLIO_RegionalSector": query(client, f"https://api-global.morningstar.com/sal-service/v1/fund/portfolio/regionalSector/{FundID}/data"),
            "GlobalAPI_PORTFOLIO_V2": query(client, f"https://api-global.morningstar.com/sal-service/v1/fund/portfolio/v2/sector/{FundID}/data"),
            # Price Data:
            "GlobalAPI_PRICE_CostIllustration": query(client, f"https://api-global.morningstar.com/sal-service/v1/fund/price/costIllustration/{FundID}/data"),
            "GlobalAPI_PRICE_FeeLevel_V1": query(client, f"https://api-global.morningstar.com/sal-service/v1/fund/price/feeLevel/v1/{FundID}/data"),
            "GlobalAPI_PRICE_FeeLevel": query(client, f"https://api-global.morningstar.com/sal-service/v1/fund/price/feeLevel/{FundID}/data"),
            "GlobalAPI_PRICE_HistoricalExpenses": query(client, f"https://api-global.morningstar.com/sal-service/v1/fund/price/historicalExpenses/{FundID}/data"),
            "GlobalAPI_PRICE_OtherFee": query(client, f"https://api-global.morningstar.com/sal-service/v1/fund/price/otherFee/{FundID}/data"),
            "GlobalAPI_PRICE_SalesFees": query(client, f"https://api-global.morningstar.com/sal-service/v1/fund/price/salesFees/{FundID}/data"),
            "GlobalAPI_PRICE_Taxes": query(client, f"https://api-global.morningstar.com/sal-service/v1/fund/price/taxes/{FundID}/data"),
            "GlobalAPI_PRICE_V4": query(client, f"https://api-global.morningstar.com/sal-service/v1/fund/price/v4/{FundID}/data"),
            # Process Data:
            "GlobalAPI_PROCESS_Asset_V2": query(client, f"https://api-global.morningstar.com/sal-service/v1/fund/process/asset/v2/{FundID}/data"),
            "GlobalAPI_PROCESS_Asset_V3": query(client, f"https://api-global.morningstar.com/sal-service/v1/fund/process/asset/v3/{FundID}/data"),
            "GlobalAPI_PROCESS_Asset": query(client, f"https://api-global.morningstar.com/sal-service/v1/fund/process/asset/{FundID}/data"),
            "GlobalAPI_PROCESS_FinancialMetrics": query(client, f"https://api-global.morningstar.com/sal-service/v1/fund/process/financialMetrics/{FundID}/data"),
            "GlobalAPI_PROCESS_MarketCap": query(client, f"https://api-global.morningstar.com/sal-service/v1/fund/process/marketCap/{FundID}/data"),
            "GlobalAPI_PROCESS_OwnershipZone": query(client, f"https://api-global.morningstar.com/sal-service/v1/fund/process/ownershipZone/{FundID}/data"),
            "GlobalAPI_PROCESS_StockStyle_V2": query(client, f"https://api-global.morningstar.com/sal-service/v1/fund/process/stockStyle/v2/{FundID}/data"),
            # Quote Data:
            "GlobalAPI_QUOTE_V3": query(client, f"https://api-global.morningstar.com/sal-service/v1/fund/quote/v3/{FundID}/data"),
            "GlobalAPI_QUOTE_V4": query(client, f"https://api-global.morningstar.com/sal-service/v1/fund/quote/v4/{FundID}/data"),
            # Security Metadata:
            "GlobalAPI_SECURITYMETADATA": query(client, f"https://api-global.morningstar.com/sal-service/v1/fund/securityMetaData/{FundID}"),
            # Strategy Preview Data:
            "GlobalAPI_STRATEGYPREVIEW": query(client, f"https://api-global.morningstar.com/sal-service/v1/fund/strategyPreview/{FundID}/data"),
            # Trailing Return Data:
            "GlobalAPI_TRAILINGRETURN_V2": query(client, f"https://api-global.morningstar.com/sal-service/v1/fund/trailingReturn/v2/{FundID}/data"),
            "GlobalAPI_TRAILINGRETURN_V3": query(client, f"https://api-global.morningstar.com/sal-service/v1/fund/trailingReturn/v3/{FundID}/data"),
            # USAPI Endpoints:
            # "USAPI_ESG_v1": query(client, f"https://www.us-api.morningstar.com/sal/sal-service/fund/esg/v1/{FundID}/data"),
            # "USAPI_FACTORPROFILE": query(client, f"https://www.us-api.morningstar.com/sal/sal-service/fund/factorProfile/{FundID}/data"),
            # "USAPI_PORTFOLIO_Holding": query(client, f"https://www.us-api.morningstar.com/sal/sal-service/fund/portfolio/holding/v2/{FundID}/data"),
            # "USAPI_PORTFOLIO_Sector": query(client, f"https://www.us-api.morningstar.com/sal/sal-service/fund/portfolio/v2/sector/{FundID}/data"),
            # "USAPI_PROCESS_Asset": query(client, f"https://www.us-api.morningstar.com/sal/sal-service/fund/process/asset/v2/{FundID}/data"),
            # "USAPI_PROCESS_FinancialMetrics": query(client, f"https://www.us-api.morningstar.com/sal/sal-service/fund/process/financialMetrics/{FundID}/data"),
            # "USAPI_PROCESS_MarketCap": query(client, f"https://www.us-api.morningstar.com/sal/sal-service/fund/process/marketCap/{FundID}/data"),
            # "USAPI_PROCESS_OwnershipZone": query(client, f"https://www.us-api.morningstar.com/sal/sal-service/fund/process/ownershipZone/{FundID}/data"),
            # "USAPI_PROCESS_StockStyle": query(client, f"https://www.us-api.morningstar.com/sal/sal-service/fund/process/stockStyle/v2/{FundID}/data"),
            # "USAPI_SECURITYMETADATA": query(client, f"https://www.us-api.morningstar.com/sal/sal-service/fund/securityMetaData/{FundID}"),
        }
        results = await asyncio.gather(*TASKS.values())

        return {key: result for key, result in zip(TASKS.keys(), results)}


def buildattr(attr_name: str, data: dict) -> dict:

    prefix = f"GlobalAPI_{attr_name}_"
    result = {}
    for key, value in data.items():
        if key.startswith(prefix):
            suffix = key[len(prefix) :]
            result[suffix] = value
    return result


class Fund:
    """
    Client for retrieving and organizing Morningstar fund data.

    Attributes:
        ESG (dict): ESG data endpoints.
        ESGRisk (dict): ESG risk data endpoints.
        FactorProfile (dict): Factor profile data endpoints.
        MorningstarTake (dict): Morningstar take data endpoints.
        MultiLevelFixedIncomeData (dict): Multi-level fixed income data endpoints.
        ParentFund (dict): Parent fund data endpoints.
        People (dict): People-related data endpoints.
        Performance (dict): Performance data endpoints.
        Portfolio (dict): Portfolio data endpoints.
        Price (dict): Price data endpoints.
        Process (dict): Process data endpoints.
        Quote (dict): Quote data endpoints.
        SecurityMetaData (dict): Security metadata endpoints.
        StrategyPreview (dict): Strategy preview data endpoints.
        TrailingReturn (dict): Trailing return data endpoints.
    """

    def __init__(self, FundID: str):
        """
        Initialize Fund client and fetch data.

        Parameters:
            FundID (str): Fund identifier string.

        Raises:
            TypeError: If FundID is not a string.
            ValueError: If FundID is empty or no data returned.
        """
        if not isinstance(FundID, str):
            raise TypeError("FundID must be a string.")
        if not FundID:
            raise ValueError("FundID cannot be empty.")

        all_data = asyncio.run(queries(FundID))
        if not all_data:
            raise ValueError("No data available.")

        self.ESG = buildattr("ESG", all_data)
        self.ESGRisk = buildattr("ESGRISK", all_data)
        self.FactorProfile = buildattr("FACTORPROFILE", all_data)
        self.MorningstarTake = buildattr("MORNINGSTARTAKE", all_data)
        self.MultiLevelFixedIncomeData = buildattr("MULTILEVELFIXEDINCOMEDATA", all_data)
        self.ParentFund = buildattr("PARENT", all_data)
        self.People = buildattr("PEOPLE", all_data)
        self.Performance = buildattr("PERFORMANCE", all_data)
        self.Portfolio = buildattr("PORTFOLIO", all_data)
        self.Price = buildattr("PRICE", all_data)
        self.Process = buildattr("PROCESS", all_data)
        self.Quote = buildattr("QUOTE", all_data)
        self.SecurityMetaData = buildattr("SECURITYMETADATA", all_data)
        self.StrategyPreview = buildattr("STRATEGYPREVIEW", all_data)
        self.TrailingReturn = buildattr("TRAILINGRETURN", all_data)
