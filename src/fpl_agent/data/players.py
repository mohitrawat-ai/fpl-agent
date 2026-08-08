"""Turn the raw bootstrap payload into flat player records."""

from dataclasses import dataclass
from typing import Any

POSITIONS = {1: "GKP", 2: "DEF", 3: "MID", 4: "FWD"}


@dataclass(frozen=True)
class Player:
    id: int
    name: str
    team: str
    position: str
    price: float  # in £m
    status: str  # a=available, i=injured, d=doubtful, s=suspended, u=unavailable
    selected_by_percent: float
    season_points: int  # current season total; 0 pre-season


def players_from_bootstrap(bootstrap: dict[str, Any]) -> list[Player]:
    teams = {t["id"]: t["short_name"] for t in bootstrap["teams"]}
    return [
        Player(
            id=e["id"],
            name=e["web_name"],
            team=teams[e["team"]],
            position=POSITIONS[e["element_type"]],
            price=e["now_cost"] / 10,
            status=e["status"],
            selected_by_percent=float(e["selected_by_percent"]),
            season_points=e["total_points"],
        )
        for e in bootstrap["elements"]
    ]
