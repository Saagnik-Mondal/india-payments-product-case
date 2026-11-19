"""Draw the charts used in the report from the CSVs in results/."""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

BLUE, RED, GREY, GREEN, AMBER = "#2f5bea", "#d64545", "#8a8a85", "#2b9a66", "#e8a33d"


def style(ax) -> None:
    ax.spines[["top", "right"]].set_visible(False)
    ax.tick_params(labelsize=8)


def label(row) -> str:
    return f"{int(row['year'])} Q{int(row['quarter'])}"


def growth(res: Path, out: Path) -> None:
    df = pd.read_csv(res / "01_national_growth.csv")
    df["period"] = df.apply(label, axis=1)
    fig, (a, b) = plt.subplots(1, 2, figsize=(11, 3.8))
    a.bar(df["period"], df["transactions_bn"], color=BLUE)
    a.set_title("Transactions per quarter (billions)", fontsize=10, loc="left")
    a.set_xticks(range(0, len(df), 4), df["period"][::4], rotation=0)
    recent = df[df["year"] >= 2021]
    b.plot(recent["period"], recent["txn_growth_yoy_pct"], color=BLUE, label="Transactions")
    b.plot(recent["period"], recent["user_growth_yoy_pct"], color=GREEN, label="Registered users")
    b.plot(
        recent["period"],
        recent["engagement_growth_yoy_pct"],
        color=AMBER,
        label="Transactions per user",
    )
    b.set_title("Year-over-year growth (%): both engines are slowing", fontsize=10, loc="left")
    b.set_xticks(range(0, len(recent), 4), recent["period"].iloc[::4], rotation=0)
    b.legend(frameon=False, fontsize=8)
    for ax in (a, b):
        style(ax)
    fig.tight_layout()
    fig.savefig(out / "01_growth.png", dpi=160)
    plt.close(fig)


def sources(res: Path, out: Path) -> None:
    df = pd.read_csv(res / "02_growth_decomposition.csv")
    fig, ax = plt.subplots(figsize=(8, 3.8))
    ax.bar(
        df["year"], df["pct_of_growth_from_more_usage"], color=AMBER, label="Users using it more"
    )
    ax.bar(
        df["year"],
        df["pct_of_growth_from_more_users"],
        bottom=df["pct_of_growth_from_more_usage"],
        color=GREEN,
        label="More registered users",
    )
    for y, t in zip(df["year"], df["txn_growth_pct"], strict=True):
        ax.text(y, 103, f"{t:.0f}%", ha="center", fontsize=8)
    ax.set_ylim(0, 112)
    ax.set_ylabel("Share of growth (%)", fontsize=9)
    ax.set_title(
        "Where growth came from (Q2 vs Q2 a year earlier; label = transaction growth)",
        fontsize=10,
        loc="left",
    )
    ax.legend(frameon=False, fontsize=8, loc="upper center", bbox_to_anchor=(0.5, -0.1), ncol=2)
    style(ax)
    fig.tight_layout()
    fig.savefig(out / "02_growth_sources.png", dpi=160)
    plt.close(fig)


def mix(res: Path, out: Path) -> None:
    df = pd.read_csv(res / "03_category_mix.csv")
    df["period"] = df.apply(label, axis=1)
    p = df.pivot(index="period", columns="category", values="share_pct")
    fig, ax = plt.subplots(figsize=(8, 3.8))
    ax.stackplot(
        range(len(p)),
        p["Retail"],
        p["P2P"],
        p["Utility"],
        labels=["Retail (merchants)", "P2P (person to person)", "Utility (bills, recharge)"],
        colors=[BLUE, AMBER, GREY],
    )
    ax.set_xticks(range(0, len(p), 4), p.index[::4])
    ax.set_ylim(0, 100)
    ax.set_xlim(0, len(p) - 1)
    ax.set_ylabel("Share of transactions (%)", fontsize=9)
    ax.set_title("What people pay for: merchant payments now lead", fontsize=10, loc="left")
    ax.legend(frameon=False, fontsize=8, loc="lower left")
    style(ax)
    fig.tight_layout()
    fig.savefig(out / "03_category_mix.png", dpi=160)
    plt.close(fig)


def states(res: Path, out: Path) -> None:
    df = pd.read_csv(res / "04_state_latest.csv").sort_values("txns_per_user")
    national = pd.read_csv(res / "01_national_growth.csv").iloc[-1]["txns_per_user"]
    fig, ax = plt.subplots(figsize=(8, 8))
    colors = [BLUE if u >= 30e6 else GREY for u in df["users"]]
    ax.barh(df["state"], df["txns_per_user"], color=colors)
    ax.axvline(national, ls="--", color=RED)
    ax.text(national + 1, 1, f"India: {national:.0f}", color=RED, fontsize=8)
    for y, v in enumerate(df["txns_per_user"]):
        ax.text(v + 0.8, y, f"{v:.0f}", va="center", fontsize=7)
    ax.set_xlabel("Transactions per registered user, latest quarter", fontsize=9)
    ax.set_title(
        "Same app, very different usage (blue = states with 30M+ users)", fontsize=10, loc="left"
    )
    ax.tick_params(axis="y", labelsize=7)
    style(ax)
    fig.tight_layout()
    fig.savefig(out / "04_state_engagement.png", dpi=160)
    plt.close(fig)


def districts(res: Path, out: Path) -> None:
    d = pd.read_csv(res / "06_district_latest.csv")
    d = d[d["users"] >= 100000]
    p25 = d["txns_per_user"].quantile(0.25)
    low = d["txns_per_user"] < p25
    fig, ax = plt.subplots(figsize=(7.5, 5))
    ax.scatter(
        d.loc[~low, "merchants_per_1000_users"],
        d.loc[~low, "txns_per_user"],
        s=10,
        color=GREY,
        alpha=0.6,
        label="Other districts",
    )
    ax.scatter(
        d.loc[low, "merchants_per_1000_users"],
        d.loc[low, "txns_per_user"],
        s=14,
        color=RED,
        alpha=0.8,
        label=f"Bottom quarter (<{p25:.0f} per user)",
    )
    rho = d["merchants_per_1000_users"].rank().corr(d["txns_per_user"].rank())
    ax.set_xlim(0, d["merchants_per_1000_users"].quantile(0.99) * 1.05)
    ax.set_xlabel("Registered merchants per 1,000 registered users", fontsize=9)
    ax.set_ylabel("Transactions per registered user", fontsize=9)
    ax.set_title(
        f"Districts: more merchants do not by themselves mean more usage (rank corr. {rho:.2f})",
        fontsize=9.5,
        loc="left",
    )
    ax.legend(frameon=False, fontsize=8)
    style(ax)
    fig.tight_layout()
    fig.savefig(out / "05_district_scatter.png", dpi=160)
    plt.close(fig)


def west_bengal(res: Path, out: Path) -> None:
    df = pd.read_csv(res / "10_west_bengal.csv").sort_values("txns_per_user")
    med = df["national_median_txns_per_user"].iloc[0]
    names = [x.replace(" district", "").title() for x in df["district"]]
    fig, ax = plt.subplots(figsize=(7.5, 6.5))
    ax.barh(
        names,
        df["txns_per_user"],
        color=[GREEN if r == "North Bengal" else GREY for r in df["region"]],
    )
    ax.axvline(med, ls="--", color=RED)
    ax.text(med + 0.5, 0.2, f"National median district: {med:.0f}", color=RED, fontsize=8)
    for y, v in enumerate(df["txns_per_user"]):
        ax.text(v + 0.5, y, f"{v:.0f}", va="center", fontsize=7)
    ax.set_xlabel("Transactions per registered user, latest quarter", fontsize=9)
    ax.set_title("West Bengal districts (green = North Bengal)", fontsize=10, loc="left")
    ax.tick_params(axis="y", labelsize=7)
    style(ax)
    fig.tight_layout()
    fig.savefig(out / "06_west_bengal.png", dpi=160)
    plt.close(fig)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--results", type=Path, default=Path("results"))
    ap.add_argument("--out", type=Path, default=Path("charts"))
    args = ap.parse_args()
    args.out.mkdir(exist_ok=True)
    for fn in (growth, sources, mix, states, districts, west_bengal):
        fn(args.results, args.out)
    print("Charts written to", args.out)


if __name__ == "__main__":
    main()
