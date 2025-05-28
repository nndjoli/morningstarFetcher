import httpx
import pandas as pd

from .Utils.Constants import FIELDS, KEYS, SITES


def reqparams(
    BrandingCompanyId=None,
    AdministratorCompanyId=None,
    CategoryId=None,
    GlobalCategoryId=None,
    GlobalAssetClassId=None,
    IMASectorID=None,
    LargestRegion=None,
    LargestSector=None,
    ShareClassTypeId=None,
    ManagementStyle=None,
    distribution=None,
    FeeLevel=None,
    OngoingCharge=None,
    CollectedSRRI=None,
    StarRatingM255=None,
    Medalist_RatingNumber=None,
    SustainabilityRank=None,
    InvestorType=None,
    Expertise=None,
    ReturnProfile=None,
):
    filters = []

    if BrandingCompanyId is not None:
        filters.append(f"BrandingCompanyId:EQ:{KEYS['BrandingCompanyId'][BrandingCompanyId]}")

    if AdministratorCompanyId is not None:
        filters.append(f"AdministratorCompanyId:EQ:{KEYS['AdministratorCompanyId'][AdministratorCompanyId]}")

    if CategoryId is not None:
        filters.append(f"CategoryId:EQ:{KEYS['CategoryId'][CategoryId]}")

    if GlobalCategoryId is not None:
        filters.append(f"GlobalCategoryId:EQ:{KEYS['GlobalCategoryId'][GlobalCategoryId]}")

    if GlobalAssetClassId is not None:
        filters.append(f"GlobalAssetClassId:EQ:{KEYS['GlobalAssetClassId'][GlobalAssetClassId]}")

    if IMASectorID is not None:
        filters.append(f"IMASectorID:IN:{KEYS['IMASectorID'][IMASectorID]}")

    if LargestRegion is not None:
        filters.append(f"LargestRegion:IN:{KEYS['LargestRegion'][LargestRegion]}")

    if LargestSector is not None:
        filters.append(f"LargestSector:IN:{KEYS['LargestSector'][LargestSector]}")

    if ShareClassTypeId is not None:
        filters.append(f"ShareClassTypeId:EQ:{KEYS['ShareClassTypeId'][ShareClassTypeId]}")

    if ManagementStyle is not None:
        filters.append(f"ManagementStyle:EQ:{KEYS['ManagementStyle'][ManagementStyle]}")

    if distribution is not None:
        filters.append(f"distribution:IN:{KEYS['distribution'][distribution]}")

    if FeeLevel is not None:
        operator = "IN" if ":" in str(FeeLevel) else "EQ"
        filters.append(f"FeeLevel:{operator}:{KEYS['FeeLevel'][FeeLevel]}")

    if OngoingCharge is not None:
        filters.append(f"OngoingCharge:EQ:{KEYS['OngoingCharge'][OngoingCharge]}")

    if CollectedSRRI is not None:
        filters.append(f"CollectedSRRI:IN:{KEYS['CollectedSRRI'][CollectedSRRI]}")

    if StarRatingM255 is not None:
        filters.append(f"StarRatingM255:IN:{KEYS['StarRatingM255'][StarRatingM255]}")

    if Medalist_RatingNumber is not None:
        filters.append(f"Medalist_RatingNumber:IN:{KEYS['Medalist_RatingNumber'][Medalist_RatingNumber]}")

    if SustainabilityRank is not None:
        filters.append(f"SustainabilityRank:IN:{KEYS['SustainabilityRank'][SustainabilityRank]}")

    if InvestorType is not None:
        filters.append(f"InvestorType:EQ:{KEYS['InvestorType'][InvestorType]}")

    if Expertise is not None:
        filters.append(f"Expertise:EQ:{KEYS['Expertise'][Expertise]}")

    if ReturnProfile is not None:
        filters.append(f"ReturnProfile:EQ:{KEYS['ReturnProfile'][ReturnProfile]}")

    query = "|".join(filters)
    return query


def screenerfunc(
    CountryName=None,
    Keyword=None,
    BrandingCompanyId=None,
    Fields=None,
    AdministratorCompanyId=None,
    CategoryId=None,
    GlobalCategoryId=None,
    GlobalAssetClassId=None,
    IMASectorID=None,
    LargestRegion=None,
    LargestSector=None,
    ShareClassTypeId=None,
    ManagementStyle=None,
    distribution=None,
    FeeLevel=None,
    OngoingCharge=None,
    CollectedSRRI=None,
    StarRatingM255=None,
    Medalist_RatingNumber=None,
    SustainabilityRank=None,
    InvestorType=None,
    Expertise=None,
    ReturnProfile=None,
    Page=1,
    sortOrder="LegalName asc",
    PageSize=10000,
):

    if CountryName is None:
        print("No country provided, defaulting to 'France'. ")
        CountryName = "France"

    if CountryName not in sorted(SITES.index):
        raise Exception(f"{CountryName} not found in the list of supported countries. The list of supported countries is: {sorted(SITES.index)}")

    if CountryName == "Taiwan":
        code = "lwbti4ryk4"
    else:
        code = "klr5zyak8x"

    if Keyword is None:
        keyword = ""
    else:
        keyword = Keyword

    if Fields is None:
        fields = "|".join(FIELDS)
    elif isinstance(Fields, list):
        for field in Fields:
            if field not in FIELDS:
                raise Exception(f"{field} is not a valid field. The list of valid fields is: {FIELDS}")
        if "SecId" not in Fields and "Name" not in Fields:
            fields = "Name|SecId|"
            fields += "|".join(Fields)
        else:
            fields = "|".join(Fields)
    else:
        raise Exception(f"Fields must be a list of strings. The list of valid fields is: {FIELDS}")

    country_base_url = SITES.loc[CountryName]["URL"]
    languageId = SITES.loc[CountryName]["languageId"]
    currencyId = SITES.loc[CountryName]["currencyId"]
    universeId = SITES.loc[CountryName]["universeIds"]

    filters = reqparams(
        BrandingCompanyId,
        AdministratorCompanyId,
        CategoryId,
        GlobalCategoryId,
        GlobalAssetClassId,
        IMASectorID,
        LargestRegion,
        LargestSector,
        ShareClassTypeId,
        ManagementStyle,
        distribution,
        FeeLevel,
        OngoingCharge,
        CollectedSRRI,
        StarRatingM255,
        Medalist_RatingNumber,
        SustainabilityRank,
        InvestorType,
        Expertise,
        ReturnProfile,
    )

    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7",
        "origin": country_base_url.replace("http", "https"),
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
    }

    params = {
        "page": Page,
        "pageSize": PageSize,
        "sortOrder": sortOrder,
        "outputType": "json",
        "version": "1",
        "languageId": languageId,
        "currencyId": currencyId,
        "universeIds": universeId,
        "securityDataPoints": fields,
        "filters": filters,
        "term": keyword,
        "subUniverseId": "",
    }
    response = httpx.get(
        f"https://tools.morningstar.co.uk/api/rest.svc/{code}/security/screener",
        headers=headers,
        params=params,
        timeout=30,
    )

    if response.status_code == 200:
        return response.json()["rows"]

    else:
        print(f"Error: {response.status_code}")
        return response.text


class ScreenerFunction:
    """
    Interface for Morningstar security screener API.

    Attributes:
        countries: DataFrame of supported countries with site settings.
        administrator_company_ids: Mapping of AdministratorCompanyId to API keys.
        branding_company_ids: Mapping of BrandingCompanyId to API keys.
        category_ids: Mapping of CategoryId to API keys.
        distribution: Mapping of distribution options to API keys.
        fee_level: Mapping of FeeLevel options to API keys.
        largest_region: Mapping of LargestRegion options to API keys.
        global_asset_class_ids: Mapping of GlobalAssetClassId to API keys.
        global_category_ids: Mapping of GlobalCategoryId to API keys.
        ima_sector_ids: Mapping of IMASectorID to API keys.
        expertise: Mapping of Expertise options to API keys.
        return_profile: Mapping of ReturnProfile options to API keys.
        investor_type: Mapping of InvestorType options to API keys.
        largest_sector: Mapping of LargestSector options to API keys.
        medalist_rating_number: Mapping of Medalist_RatingNumber to API keys.
        ongoing_charge: Mapping of OngoingCharge options to API keys.
        collected_srri: Mapping of CollectedSRRI options to API keys.
        share_class_type_ids: Mapping of ShareClassTypeId to API keys.
        star_ratingM255: Mapping of StarRatingM255 options to API keys.
        sustainability_rank: Mapping of SustainabilityRank options to API keys.
        umbrella_company_ids: Mapping of UmbrellaCompanyId to API keys.
        FIELDS: List of valid data fields for queries.
        SITES: DataFrame of supported countries with site settings.
        KEYS: Dictionary of filter key mappings.
    """

    def __init__(self):
        """
        Load filter key mappings and valid fields.
        """
        self.countries = SITES
        self.administrator_company_ids = KEYS["AdministratorCompanyId"]
        self.branding_company_ids = KEYS["BrandingCompanyId"]
        self.category_ids = KEYS["CategoryId"]
        self.distribution = KEYS["distribution"]
        self.fee_level = KEYS["FeeLevel"]
        self.largest_region = KEYS["LargestRegion"]
        self.global_asset_class_ids = KEYS["GlobalAssetClassId"]
        self.global_category_ids = KEYS["GlobalCategoryId"]
        self.ima_sector_ids = KEYS["IMASectorID"]
        self.expertise = KEYS["Expertise"]
        self.return_profile = KEYS["ReturnProfile"]
        self.investor_type = KEYS["InvestorType"]
        self.largest_sector = KEYS["LargestSector"]
        self.medalist_rating_number = KEYS["Medalist_RatingNumber"]
        self.ongoing_charge = KEYS["OngoingCharge"]
        self.collected_srri = KEYS["CollectedSRRI"]
        self.share_class_type_ids = KEYS["ShareClassTypeId"]
        self.star_ratingM255 = KEYS["StarRatingM255"]
        self.sustainability_rank = KEYS["SustainabilityRank"]
        self.umbrella_company_ids = KEYS["UmbrellaCompanyId"]
        self.FIELDS = FIELDS
        self.SITES = SITES
        self.KEYS = KEYS

    def screener(
        self,
        CountryName=None,
        Keyword=None,
        BrandingCompanyId=None,
        Fields=None,
        AdministratorCompanyId=None,
        CategoryId=None,
        GlobalCategoryId=None,
        GlobalAssetClassId=None,
        IMASectorID=None,
        LargestRegion=None,
        LargestSector=None,
        ShareClassTypeId=None,
        ManagementStyle=None,
        distribution=None,
        FeeLevel=None,
        OngoingCharge=None,
        CollectedSRRI=None,
        StarRatingM255=None,
        Medalist_RatingNumber=None,
        SustainabilityRank=None,
        InvestorType=None,
        Expertise=None,
        ReturnProfile=None,
        Page=1,
        sortOrder="LegalName asc",
        PageSize=10000,
    ):
        """
        Query Morningstar screener endpoint and return DataFrame.

        Parameters:
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

        Returns:
            pandas.DataFrame: Screener results.

        Raises:
            Exception: If CountryName unsupported or Fields invalid.
        """
        data = screenerfunc(
            CountryName,
            Keyword,
            BrandingCompanyId,
            Fields,
            AdministratorCompanyId,
            CategoryId,
            GlobalCategoryId,
            GlobalAssetClassId,
            IMASectorID,
            LargestRegion,
            LargestSector,
            ShareClassTypeId,
            ManagementStyle,
            distribution,
            FeeLevel,
            OngoingCharge,
            CollectedSRRI,
            StarRatingM255,
            Medalist_RatingNumber,
            SustainabilityRank,
            InvestorType,
            Expertise,
            ReturnProfile,
            Page=Page,
            sortOrder=sortOrder,
            PageSize=PageSize,
        )
        return pd.DataFrame(data)
