import json

import morningstarFetcher

# ScreenerFunction test:
screener_test = morningstarFetcher.ScreenerFunction().screener(
    "France", "Technology", Fields=["GBRReturnM12"]
)
screener_test_json = screener_test.to_dict(orient="records")

with open(
    "morningstarFetcher/tests/screener_test.json", "w", encoding="utf-8"
) as f:
    json.dump(screener_test_json, f, indent=4)


# Fund test:
fund_test = morningstarFetcher.Fund("F0GBR04I8U")
fund_test_json = fund_test.__dict__


with open(
    "morningstarFetcher/tests/fund_test.json", "w", encoding="utf-8"
) as f:
    json.dump(fund_test_json, f, indent=4)
