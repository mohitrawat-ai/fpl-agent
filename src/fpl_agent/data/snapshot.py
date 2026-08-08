"""Snapshot the live FPL API to data/raw/<date>/.

Usage: uv run python -m fpl_agent.data.snapshot
"""

import datetime
import json
from pathlib import Path

import httpx

from fpl_agent.data.fpl_api import fetch_bootstrap, fetch_fixtures
from fpl_agent.data.players import players_from_bootstrap

RAW_DIR = Path("data/raw")


def main() -> None:
    today = datetime.datetime.now(tz=datetime.UTC).date().isoformat()
    out = RAW_DIR / today
    out.mkdir(parents=True, exist_ok=True)

    with httpx.Client(timeout=30) as client:
        bootstrap = fetch_bootstrap(client)
        fixtures = fetch_fixtures(client)

    (out / "bootstrap.json").write_text(json.dumps(bootstrap))
    (out / "fixtures.json").write_text(json.dumps(fixtures))

    players = players_from_bootstrap(bootstrap)
    events = bootstrap["events"]
    next_deadline = next((e for e in events if e["is_next"]), None)
    print(f"snapshot -> {out}")
    print(f"players: {len(players)}, fixtures: {len(fixtures)}, gameweeks: {len(events)}")
    if next_deadline:
        print(f"next deadline: {next_deadline['name']} at {next_deadline['deadline_time']}")


if __name__ == "__main__":
    main()
