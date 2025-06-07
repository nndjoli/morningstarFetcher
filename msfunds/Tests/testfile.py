import msfunds
import json


# ScreenerFunction test:
screener_test = msfunds.ScreenerFunction().screener("France", "Technology", Fields=["GBRReturnM12"])
screener_test_json = screener_test.to_dict(orient="records")

with open("msfunds/Tests/screener_test.json", "w", encoding="utf-8") as f:
    json.dump(screener_test_json, f, indent=4)


# Fund test:
fund_test = msfunds.Fund("F0GBR04I8U")
fund_test_json = fund_test.__dict__


with open("msfunds/Tests/fund_test.json", "w", encoding="utf-8") as f:
    json.dump(fund_test_json, f, indent=4)
