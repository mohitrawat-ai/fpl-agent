from fpl_agent.data.core_insights import team_elos

TEAMS_CSV = """code,id,name,short_name,strength,elo,fotmob_name
3,1,Arsenal,ARS,4,1955.3,Arsenal
7,2,Aston Villa,AVL,3,1802.0,Aston Villa
"""

# Pre-season shape: elo column exists but is unpopulated.
TEAMS_CSV_EMPTY_ELO = """code,id,name,short_name,strength,elo,fotmob_name
3,1,Arsenal,ARS,4,,Arsenal
7,2,Aston Villa,AVL,3,1802.0,Aston Villa
"""


def test_team_elos_maps_short_name_to_rating():
    elos = team_elos(TEAMS_CSV)
    assert elos == {"ARS": 1955.3, "AVL": 1802.0}


def test_team_elos_omits_empty_cells():
    elos = team_elos(TEAMS_CSV_EMPTY_ELO)
    assert elos == {"AVL": 1802.0}
