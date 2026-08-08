"""Normalize vaastav per-GW history into one standard row shape for backtesting.

Source: https://github.com/vaastav/Fantasy-Premier-League (history only; weekly
updates stopped after 2024-25). Seasons before 2020-21 lack team/position columns
and use older scoring rules, so the ingest starts at 2020-21.

One output row = one player in one fixture. Double gameweeks produce two rows
with the same gw value.

Usage: uv run python -m fpl_agent.data.history
"""

import csv
import io
from pathlib import Path
from typing import Any

import httpx

RAW_BASE = (
    "https://raw.githubusercontent.com/vaastav/Fantasy-Premier-League/master/data"
)
SEASONS = ("2020-21", "2021-22", "2022-23", "2023-24", "2024-25")

VAASTAV_DIR = Path("data/raw/vaastav")
HISTORY_DIR = Path("data/history")

# Standard schema. Order matters: identity, pre-kickoff context, ground truth, signals.
FIELDS = [
    "season",
    "gw",
    "element",
    "name",
    "position",
    "team",
    "opponent",
    "was_home",
    "kickoff_time",
    "price",
    "selected",
    "minutes",
    "total_points",
    "goals_scored",
    "assists",
    "clean_sheets",
    "goals_conceded",
    "bonus",
    "bps",
    "saves",
    "starts",
    "xp",
    "xg",
    "xa",
    "xgc",
]

POSITIONS = {"GK": "GKP", "GKP": "GKP", "DEF": "DEF", "MID": "MID", "FWD": "FWD"}


def _fetch_cached(client: httpx.Client, season: str, filename: str) -> str:
    """Download a vaastav file once; reuse the local copy afterwards."""
    path = VAASTAV_DIR / season / filename
    if path.exists():
        return path.read_text()
    resp = client.get(f"{RAW_BASE}/{season}/{filename}")
    resp.raise_for_status()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(resp.text)
    return resp.text


def team_short_names(teams_csv: str) -> tuple[dict[int, str], dict[str, str]]:
    """Two lookups: team id -> short name, full name -> short name."""
    by_id: dict[int, str] = {}
    by_name: dict[str, str] = {}
    for row in csv.DictReader(io.StringIO(teams_csv)):
        by_id[int(row["id"])] = row["short_name"]
        by_name[row["name"]] = row["short_name"]
    return by_id, by_name


def normalize_rows(
    season: str,
    merged_gw_csv: str,
    team_by_id: dict[int, str],
    team_by_name: dict[str, str],
) -> tuple[list[dict[str, Any]], int]:
    """Map raw vaastav rows onto FIELDS. Returns (rows, dropped_count).

    Drops rows whose position is not one of the four player positions
    (2024-25 has assistant-manager rows).
    """
    rows: list[dict[str, Any]] = []
    dropped = 0
    for raw in csv.DictReader(io.StringIO(merged_gw_csv)):
        position = POSITIONS.get(raw["position"])
        if position is None:
            dropped += 1
            continue
        rows.append(
            {
                "season": season,
                "gw": int(raw["GW"]),
                "element": int(raw["element"]),
                "name": raw["name"],
                "position": position,
                "team": team_by_name[raw["team"]],
                "opponent": team_by_id[int(raw["opponent_team"])],
                "was_home": raw["was_home"] == "True",
                "kickoff_time": raw["kickoff_time"],
                "price": int(raw["value"]) / 10,
                "selected": int(raw["selected"]),
                "minutes": int(raw["minutes"]),
                "total_points": int(raw["total_points"]),
                "goals_scored": int(raw["goals_scored"]),
                "assists": int(raw["assists"]),
                "clean_sheets": int(raw["clean_sheets"]),
                "goals_conceded": int(raw["goals_conceded"]),
                "bonus": int(raw["bonus"]),
                "bps": int(raw["bps"]),
                "saves": int(raw["saves"]),
                "starts": raw.get("starts", ""),
                "xp": raw.get("xP", ""),
                "xg": raw.get("expected_goals", ""),
                "xa": raw.get("expected_assists", ""),
                "xgc": raw.get("expected_goals_conceded", ""),
            }
        )
    return rows, dropped


def main() -> None:
    HISTORY_DIR.mkdir(parents=True, exist_ok=True)
    with httpx.Client(timeout=60) as client:
        for season in SEASONS:
            teams_csv = _fetch_cached(client, season, "teams.csv")
            merged_csv = _fetch_cached(client, season, "gws/merged_gw.csv")
            by_id, by_name = team_short_names(teams_csv)
            rows, dropped = normalize_rows(season, merged_csv, by_id, by_name)

            out = HISTORY_DIR / f"{season}.csv"
            with out.open("w", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=FIELDS)
                writer.writeheader()
                writer.writerows(rows)

            gws = {r["gw"] for r in rows}
            note = f", dropped {dropped} non-player rows" if dropped else ""
            print(
                f"{season}: {len(rows)} rows, GW {min(gws)}-{max(gws)} -> {out}{note}"
            )


if __name__ == "__main__":
    main()
