import asyncio

import httpx

# Mapping of universe codes to field keywords used in ``fields`` metadata
_CODE_TO_FIELD_KEYWORD = {
    "EQ": "stocks",
    "FE": "etfs",
    "FO": "mutual funds",
}


async def query(client, url):
    response = await client.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Error fetching data from {url}: {response.status_code}")


async def screener_builders(headers=None):
    async with httpx.AsyncClient(headers=headers) as client:
        tasks = {
            "country_codes": query(
                client,
                "https://global.morningstar.com/api/v1/en-eu/stores/country-codes",
            ),
            "editions": query(
                client,
                "https://global.morningstar.com/api/v1/en-eu/stores/editions",
            ),
            "markets": query(
                client,
                "https://global.morningstar.com/api/v1/en-eu/stores/markets",
            ),
            "languages": query(
                client,
                "https://global.morningstar.com/api/v1/en-eu/stores/languages",
            ),
            "fields_en_eu": query(
                client,
                "https://global.morningstar.com/api/v1/en-eu/stores/data-points/fields?private=true",
            ),
            "fields_fr": query(
                client,
                "https://global.morningstar.com/api/v1/fr/stores/data-points/fields?private=true",
            ),
            "fields_us": query(
                client,
                "https://www.morningstar.com/api/v2/stores/data-points/fields",
            ),
            "views": query(
                client,
                "https://global.morningstar.com/api/v1/en-eu/stores/views",
            ),
            "filters": query(
                client,
                "https://global.morningstar.com/api/v1/en-eu/stores/filters",
            ),
            "documents": query(
                client,
                "https://global.morningstar.com/api/v1/en-eu/stores/documents",
            ),
        }
        results = await asyncio.gather(*tasks.values())
        response = {key: result for key, result in zip(tasks.keys(), results)}
        response["fields"] = []

        for key in ["fields_en_eu", "fields_fr", "fields_us"]:
            if key in response:
                response["fields"].extend(response[key].get("results", []))

        del response["fields_en_eu"]
        del response["fields_fr"]
        del response["fields_us"]

        return response


def process_markets_response(markets_response):
    markets_by_id = markets_response["marketsById"]
    result = {}
    for name, m in markets_by_id.items():
        new_m = m.copy()
        queries = new_m.pop("universeQueries")
        new_m["queries"] = {q["universe"]: q for q in queries}
        result[name] = new_m
    return result


def process_filters_response(filters_response):
    processed_response = {}

    for filt in filters_response["results"]:
        key = ",".join(filt["universes"])
        if key not in processed_response:
            processed_response[key] = {}

            for category in filt["filters"]:
                cat_id = category["id"]
                children_dict = {}

                for child in category["children"]:
                    field_name = child["field"]
                    info = {k: v for k, v in child.items() if k != "field"}
                    children_dict[field_name] = info

                processed_response[key][cat_id] = children_dict

    return processed_response


def get_market(market_id, processed_markets):
    if market_id in processed_markets:
        return processed_markets[market_id]
    else:
        raise ValueError(f"Market ID {market_id} not found. Available IDs: {list(processed_markets.keys())}")


def process_views_response(views_response, market_country_codes):
    processed_views = {}

    for view in views_response["results"]:
        universes = view.get("universes") or []
        if not universes or not universes[0]:
            continue
        universe = universes[0]
        processed_views.setdefault(universe, {})
        name = view.get("name")
        if not name or name == "Unnamed":
            continue

        fields = view.get("fields", [])

        view_fields = []
        for field in fields:
            val = field.get("field")
            if val in ["fundSizeDate", "priipsKidCostsDate", "lastPrice"]:
                continue
            var = field.get("variation")

            country_codes = field.get("countryCodes", [])

            if country_codes:
                if market_country_codes[0] not in country_codes:
                    continue

            if val:
                view_fields.append(f"{val}[{var}]" if var else val)

        processed_views[universe][name.lower().replace(" & ", "_")] = ",".join(view_fields)

    return processed_views


def process_query_response(response):
    flat_records = []
    for item in response["results"]:
        flattened = dict(item["meta"])
        for key, content in item["fields"].items():
            # Always extract the main value
            flattened[key] = content.get("value")
            # If there are nested properties, extract them too
            props = content.get("properties", {})
            for prop_name, prop_content in props.items():
                flattened[f"{key}_{prop_name}"] = prop_content.get("value")
        flat_records.append(flattened)

    return flat_records


def universe_fields(fields_response, universe_id):
    """Return mapping of field name to type for a universe."""
    keyword = _CODE_TO_FIELD_KEYWORD.get(universe_id)

    fields_map = {}

    for field in fields_response:
        if "keywords" in field and keyword in field["keywords"]:
            base = field.get("field")
            ftype = field.get("attributes", {}).get("type")
            variations = field.get("variations") or []
            if variations:
                for variation in variations:
                    var = variation.get("variation")
                    if var:
                        fields_map[f"{base}[{var}]"] = ftype
            else:
                if base:
                    fields_map[base] = ftype

    meta = ["securityID", "universe", "name", "isin", "ticker", "domicile"]

    meta = [f for f in meta if f in fields_map]
    rest = sorted(k for k in fields_map if k not in meta)
    ordered = {k: fields_map[k] for k in meta + rest}

    return ordered
