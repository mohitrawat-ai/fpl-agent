"""Snapshot FPL-Core-Insights, the current-season enriched source.

Source: https://github.com/olbauday/FPL-Core-Insights. FPL API data fused with
per-match stats and ClubElo ratings, aligned on official FPL IDs. Updates
continuously, so every pull is date-stamped under data/raw/core_insights/.

Usage:
    uv run python -m fpl_agent.data.core_insights          # season-level files
    uv run python -m fpl_agent.data.core_insights 1        # ... plus GW1 files
"""

import csv
import datetime
import io
import sys
from pathlib import Path

import httpx

RAW_BASE = "https://raw.githubusercontent.com/olbauday/FPL-Core-Insights/main/data"
SEASON = "2026-2027"
# Elo prior for early gameweeks: the current season's elo column stays empty until
# their pipeline runs, and promoted clubs have no PL Elo history at all.
PRIOR_SEASON = "2025-2026"

CORE_FILES = ("players.csv", "playerstats.csv", "teams.csv", "gameweek_summaries.csv")
GW_FILES = ("fixtures.csv", "matches.csv", "playermatchstats.csv")

RAW_DIR = Path("data/raw/core_insights")


def _fetch(client: httpx.Client, season: str, relpath: str, out: Path) -> str:
    resp = client.get(f"{RAW_BASE}/{season}/{relpath}")
    resp.raise_for_status()
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(resp.text)
    return resp.text


def team_elos(teams_csv: str) -> dict[str, float]:
    """Team short name -> Elo rating. Teams with an empty elo cell are omitted."""
    return {
        row["short_name"]: float(row["elo"])
        for row in csv.DictReader(io.StringIO(teams_csv))
        if row["elo"]
    }


def main() -> None:
    gw = int(sys.argv[1]) if len(sys.argv) > 1 else None
    today = datetime.datetime.now(tz=datetime.UTC).date().isoformat()
    out_dir = RAW_DIR / today

    with httpx.Client(timeout=60) as client:
        core = {
            name: _fetch(client, SEASON, name, out_dir / name) for name in CORE_FILES
        }
        prior_teams = _fetch(
            client, PRIOR_SEASON, "teams.csv", out_dir / "teams_prior.csv"
        )
        if gw is not None:
            for name in GW_FILES:
                relpath = f"By Gameweek/GW{gw}/{name}"
                _fetch(client, SEASON, relpath, out_dir / relpath)

    players = list(csv.DictReader(io.StringIO(core["players.csv"])))
    teams = [r["short_name"] for r in csv.DictReader(io.StringIO(core["teams.csv"]))]
    elos = team_elos(core["teams.csv"]) or team_elos(prior_teams)
    covered = [t for t in teams if t in elos]
    missing = [t for t in teams if t not in elos]
    print(f"snapshot -> {out_dir}")
    print(f"players: {len(players)}, teams: {len(teams)}")
    print(f"elo coverage: {len(covered)}/{len(teams)}, missing: {missing or 'none'}")
    if gw is not None:
        print(f"gameweek files: GW{gw} -> {', '.join(GW_FILES)}")


if __name__ == "__main__":
    main()
