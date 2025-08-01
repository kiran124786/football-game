# backend/api_thesportsdb.py

import requests

BASE_URL = "https://www.thesportsdb.com/api/v1/json/1"  # '1' is default free key

# === Search a team by name ===
def search_team(team_name):
    url = f"{BASE_URL}/searchteams.php"
    params = {"t": team_name}
    response = requests.get(url, params=params)
    return response.json()

# === Get all teams in a league ===
def get_teams_in_league(league_name):
    url = f"{BASE_URL}/search_all_teams.php"
    params = {"l": league_name}
    response = requests.get(url, params=params)
    return response.json()

# === Search a player by name ===
def search_player(player_name):
    url = f"{BASE_URL}/searchplayers.php"
    params = {"p": player_name}
    response = requests.get(url, params=params)
    return response.json()

# === Get next fixtures for a team ===
def get_next_events(team_id):
    url = f"{BASE_URL}/eventsnext.php"
    params = {"id": team_id}
    response = requests.get(url, params=params)
    return response.json()

# === Get last results for a team ===
def get_last_results(team_id):
    url = f"{BASE_URL}/eventslast.php"
    params = {"id": team_id}
    response = requests.get(url, params=params)
    return response.json()
