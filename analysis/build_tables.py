"""Flatten the Pulse JSON files into CSV tables in data/tables/ for SQL.

Tables (one row per place and quarter):
    national_category   category counts for India (P2P, Retail, Utility)
    state_category      the same by state
    state_txn           transactions count and amount by state
    district_txn        transactions count and amount by district
    national_users      registered users for India
    state_users         registered users by state
    district_users      registered users by district
    state_merchants     registered merchants by state
    district_merchants  registered merchants by district
"""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

ROOT = Path("data/pulse")
OUT = Path("data/tables")
IND = "country/india"


def name(raw: str) -> str:
    """Directory names use hyphens ('west-bengal'); normalise to 'west bengal'."""
    return raw.replace("-", " ")


def periods(folder: Path):
    """Yield (year, quarter, path) for every <year>/<quarter>.json under a folder."""
    for ydir in sorted(p for p in folder.iterdir() if p.is_dir() and p.name.isdigit()):
        for f in sorted(ydir.glob("*.json")):
            yield int(ydir.name), int(f.stem), f


def load(path: Path) -> dict:
    return json.loads(path.read_text())["data"]


def category_rows(data: dict) -> list[tuple[str, int]]:
    return [(c["name"], c["paymentInstruments"][0]["count"]) for c in data["transactionData"]]


def build() -> dict[str, pd.DataFrame]:
    t: dict[str, list[dict]] = {
        k: []
        for k in (
            "national_category",
            "state_category",
            "state_txn",
            "district_txn",
            "national_users",
            "state_users",
            "district_users",
            "state_merchants",
            "district_merchants",
        )
    }

    for y, q, f in periods(ROOT / f"aggregated/transaction/{IND}"):
        for cat, n in category_rows(load(f)):
            t["national_category"].append(dict(year=y, quarter=q, category=cat, count=n))
    for y, q, f in periods(ROOT / f"aggregated/user/{IND}"):
        t["national_users"].append(
            dict(year=y, quarter=q, registered_users=load(f)["aggregated"]["registeredCount"])
        )
    for y, q, f in periods(ROOT / f"map/transaction/hover/{IND}"):
        for row in load(f)["hoverDataList"]:
            m = row["metric"][0]
            t["state_txn"].append(
                dict(state=row["name"], year=y, quarter=q, count=m["count"], amount=m["amount"])
            )
    for y, q, f in periods(ROOT / f"map/user/hover/{IND}"):
        for state, v in load(f)["hoverData"].items():
            t["state_users"].append(
                dict(state=state, year=y, quarter=q, registered_users=v["registeredCount"])
            )
    for y, q, f in periods(ROOT / f"map/merchant/hover/{IND}"):
        for state, v in load(f)["hoverData"].items():
            t["state_merchants"].append(
                dict(state=state, year=y, quarter=q, registered_merchants=v["registeredCount"])
            )

    for sdir in sorted((ROOT / f"aggregated/transaction/{IND}/state").iterdir()):
        for y, q, f in periods(sdir):
            for cat, n in category_rows(load(f)):
                t["state_category"].append(
                    dict(state=name(sdir.name), year=y, quarter=q, category=cat, count=n)
                )
    for sdir in sorted((ROOT / f"map/transaction/hover/{IND}/state").iterdir()):
        for y, q, f in periods(sdir):
            for row in load(f)["hoverDataList"]:
                m = row["metric"][0]
                t["district_txn"].append(
                    dict(
                        state=name(sdir.name),
                        district=row["name"],
                        year=y,
                        quarter=q,
                        count=m["count"],
                        amount=m["amount"],
                    )
                )
    for sdir in sorted((ROOT / f"map/user/hover/{IND}/state").iterdir()):
        for y, q, f in periods(sdir):
            for district, v in load(f)["hoverData"].items():
                t["district_users"].append(
                    dict(
                        state=name(sdir.name),
                        district=district,
                        year=y,
                        quarter=q,
                        registered_users=v["registeredCount"],
                    )
                )
    for sdir in sorted((ROOT / f"map/merchant/hover/{IND}/state").iterdir()):
        for y, q, f in periods(sdir):
            for district, v in load(f)["hoverData"].items():
                t["district_merchants"].append(
                    dict(
                        state=name(sdir.name),
                        district=district,
                        year=y,
                        quarter=q,
                        registered_merchants=v["registeredCount"],
                    )
                )
    return {k: pd.DataFrame(v) for k, v in t.items()}


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for key, df in build().items():
        df.to_csv(OUT / f"{key}.csv", index=False)
        print(f"{key:20s} {len(df):>8,} rows")


if __name__ == "__main__":
    main()
