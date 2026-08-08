from fpl_agent.data.players import Player, players_from_bootstrap

BOOTSTRAP = {
    "teams": [{"id": 1, "short_name": "ARS"}, {"id": 2, "short_name": "LIV"}],
    "elements": [
        {
            "id": 101,
            "web_name": "Saka",
            "team": 1,
            "element_type": 3,
            "now_cost": 105,
            "status": "a",
            "selected_by_percent": "45.3",
            "total_points": 0,
        },
        {
            "id": 202,
            "web_name": "Salah",
            "team": 2,
            "element_type": 3,
            "now_cost": 132,
            "status": "d",
            "selected_by_percent": "60.1",
            "total_points": 0,
        },
    ],
}


def test_players_from_bootstrap():
    players = players_from_bootstrap(BOOTSTRAP)
    assert players == [
        Player(101, "Saka", "ARS", "MID", 10.5, "a", 45.3, 0),
        Player(202, "Salah", "LIV", "MID", 13.2, "d", 60.1, 0),
    ]
