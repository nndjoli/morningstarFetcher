import json
import os
from pathlib import Path

import pandas as pd

try:
    from importlib.resources import as_file, files

    package_path = files("morningstarFetcher.Utils")

    with as_file(package_path.joinpath("Fields.json")) as fp:
        with open(fp, "r", encoding="utf-8") as f:
            FIELDS = json.load(f)

    with as_file(package_path.joinpath("Keys.json")) as kp:
        with open(kp, "r", encoding="utf-8") as f:
            KEYS = json.load(f)

    with as_file(package_path.joinpath("Sites.json")) as sp:
        with open(sp, "r", encoding="utf-8") as f:
            SITES = pd.DataFrame(json.load(f)).T

    with as_file(package_path.joinpath("URLs.json")) as up:
        with open(up, "r", encoding="utf-8") as f:
            URLS = json.load(f)

except (ImportError, ModuleNotFoundError):
    current_dir = Path(os.path.dirname(os.path.abspath(__file__)))

    with open(current_dir / "Fields.json", "r", encoding="utf-8") as f:
        FIELDS = json.load(f)

    with open(current_dir / "Keys.json", "r", encoding="utf-8") as f:
        KEYS = json.load(f)

    with open(current_dir / "Sites.json", "r", encoding="utf-8") as f:
        SITES = pd.DataFrame(json.load(f)).T

    with open(current_dir / "URLs.json", "r", encoding="utf-8") as f:
        URLS = json.load(f)
