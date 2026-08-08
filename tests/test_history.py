from fpl_agent.data.history import FIELDS, normalize_rows, team_short_names

TEAMS_CSV = """code,id,name,short_name
3,1,Arsenal,ARS
7,2,Aston Villa,AVL
"""

# 2020-21 era: position "GK", no starts/xG columns.
MERGED_2020 = """name,position,team,xP,element,opponent_team,kickoff_time,minutes,selected,total_points,goals_scored,assists,clean_sheets,goals_conceded,bonus,bps,saves,value,was_home,GW
Bernd Leno,GK,Arsenal,3.5,1,2,2020-09-12T11:30:00Z,90,100000,6,0,0,1,0,0,25,3,50,True,1
"""

# 2024-25 era: assistant-manager row must be dropped, xG columns present.
MERGED_2024 = """name,position,team,xP,element,opponent_team,kickoff_time,minutes,selected,total_points,goals_scored,assists,clean_sheets,goals_conceded,bonus,bps,saves,starts,expected_goals,expected_assists,expected_goals_conceded,value,was_home,GW
Bukayo Saka,MID,Arsenal,5.2,7,2,2024-08-17T14:00:00Z,90,5000000,8,1,0,0,1,2,40,0,1,0.45,0.20,0.90,100,False,1
Mikel Arteta,AM,Arsenal,0.0,900,2,2024-08-17T14:00:00Z,0,1000,2,0,0,0,1,0,0,0,0,0.0,0.0,0.0,15,False,1
"""


def test_normalizes_2020_era_row():
    by_id, by_name = team_short_names(TEAMS_CSV)
    rows, dropped = normalize_rows("2020-21", MERGED_2020, by_id, by_name)
    assert dropped == 0
    [row] = rows
    assert list(row) == FIELDS
    assert row["position"] == "GKP"  # "GK" normalized
    assert row["team"] == "ARS"
    assert row["opponent"] == "AVL"
    assert row["price"] == 5.0
    assert row["was_home"] is True
    assert row["total_points"] == 6
    assert row["xg"] == ""  # absent pre-2022-23 stays empty, not zero


def test_drops_assistant_manager_rows():
    by_id, by_name = team_short_names(TEAMS_CSV)
    rows, dropped = normalize_rows("2024-25", MERGED_2024, by_id, by_name)
    assert dropped == 1
    [row] = rows
    assert row["name"] == "Bukayo Saka"
    assert row["was_home"] is False
    assert row["starts"] == "1"
    assert row["xg"] == "0.45"
