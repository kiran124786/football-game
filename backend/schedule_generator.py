# backend/schedule_generator.py

import random

def generate_fixtures(teams):
    """
    Generate a round-robin schedule (each team plays each other once).
    Returns a list of matchdays with fixtures.
    """
    if len(teams) % 2 != 0:
        teams.append("BYE")  # Add dummy team for odd number of teams

    num_teams = len(teams)
    num_rounds = num_teams - 1
    half = num_teams // 2

    schedule = []
    team_list = list(teams)

    for round_num in range(num_rounds):
        round_matches = []
        for i in range(half):
            home = team_list[i]
            away = team_list[-i - 1]
            if home != "BYE" and away != "BYE":
                round_matches.append({"matchday": round_num + 1, "home": home, "away": away})
        # Rotate teams
        team_list = [team_list[0]] + [team_list[-1]] + team_list[1:-1]
        schedule.append(round_matches)

    return schedule

def shuffle_fixtures(schedule):
    """
    Randomize match order within each matchday.
    """
    for round_matches in schedule:
        random.shuffle(round_matches)
    return schedule

def get_fixtures_by_round(schedule, matchday):
    """
    Get all matches in a given round (matchday number).
    """
    if 1 <= matchday <= len(schedule):
        return schedule[matchday - 1]
    return {"error": "Invalid matchday"}
