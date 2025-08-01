# backend/league_system.py

import uuid

# Initial empty league table (replace with DB or Firebase later)
LEAGUE_TABLE = {}

def initialize_league(teams):
    """
    Create initial league table for all clubs.
    """
    global LEAGUE_TABLE
    LEAGUE_TABLE = {}
    for team in teams:
        LEAGUE_TABLE[team] = {
            "team": team,
            "played": 0,
            "won": 0,
            "drawn": 0,
            "lost": 0,
            "goals_for": 0,
            "goals_against": 0,
            "goal_diff": 0,
            "points": 0
        }
    return list(LEAGUE_TABLE.values())

def update_league_table(team_a, team_b, score_a, score_b):
    """
    Update the table after a match result.
    """
    if team_a not in LEAGUE_TABLE or team_b not in LEAGUE_TABLE:
        return {"error": "One or both teams not in league"}

    # Update matches played
    LEAGUE_TABLE[team_a]["played"] += 1
    LEAGUE_TABLE[team_b]["played"] += 1

    # Update goals
    LEAGUE_TABLE[team_a]["goals_for"] += score_a
    LEAGUE_TABLE[team_a]["goals_against"] += score_b
    LEAGUE_TABLE[team_b]["goals_for"] += score_b
    LEAGUE_TABLE[team_b]["goals_against"] += score_a

    LEAGUE_TABLE[team_a]["goal_diff"] = (
        LEAGUE_TABLE[team_a]["goals_for"] - LEAGUE_TABLE[team_a]["goals_against"]
    )
    LEAGUE_TABLE[team_b]["goal_diff"] = (
        LEAGUE_TABLE[team_b]["goals_for"] - LEAGUE_TABLE[team_b]["goals_against"]
    )

    # Update results
    if score_a > score_b:
        LEAGUE_TABLE[team_a]["won"] += 1
        LEAGUE_TABLE[team_b]["lost"] += 1
        LEAGUE_TABLE[team_a]["points"] += 3
    elif score_b > score_a:
        LEAGUE_TABLE[team_b]["won"] += 1
        LEAGUE_TABLE[team_a]["lost"] += 1
        LEAGUE_TABLE[team_b]["points"] += 3
    else:
        LEAGUE_TABLE[team_a]["drawn"] += 1
        LEAGUE_TABLE[team_b]["drawn"] += 1
        LEAGUE_TABLE[team_a]["points"] += 1
        LEAGUE_TABLE[team_b]["points"] += 1

    return {"message": "League table updated"}

def get_league_table():
    """
    Return sorted league table by points, then goal difference.
    """
    return sorted(
        LEAGUE_TABLE.values(),
        key=lambda x: (x["points"], x["goal_diff"], x["goals_for"]),
        reverse=True
    )
