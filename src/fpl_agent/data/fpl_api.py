"""Read-only client for the official FPL API.

Endpoints are undocumented but stable. Reference:
https://www.oliverlooney.com/blogs/FPL-APIs-Explained
"""

from typing import Any

import httpx

BASE_URL = "https://fantasy.premierleague.com/api"


def fetch_bootstrap(client: httpx.Client) -> dict[str, Any]:
    """The main payload: all players, teams, prices, form, ownership, gameweeks."""
    resp = client.get(f"{BASE_URL}/bootstrap-static/")
    resp.raise_for_status()
    return resp.json()


def fetch_fixtures(client: httpx.Client) -> list[dict[str, Any]]:
    """All fixtures for the season, with difficulty ratings."""
    resp = client.get(f"{BASE_URL}/fixtures/")
    resp.raise_for_status()
    return resp.json()


def fetch_player_history(client: httpx.Client, player_id: int) -> dict[str, Any]:
    """Per-gameweek history and upcoming fixtures for one player."""
    resp = client.get(f"{BASE_URL}/element-summary/{player_id}/")
    resp.raise_for_status()
    return resp.json()
