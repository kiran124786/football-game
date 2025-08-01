# backend/player_manager.py

import random
import uuid

# === Player Transfer ===
def transfer_player(player_id, from_team, to_team):
    """
    Simulate a player transfer by moving player ID between teams.
    """
    # In real backend, you'd fetch and update DB records.
    return {
        "message": f"Player {player_id} transferred from {from_team} to {to_team}."
    }

# === Youth Player Generation ===
def generate_youth_player():
    """
    Generate a youth player with random stats and unique ID.
    """
    positions = ["ST", "CM", "CB", "GK", "LM", "RM", "RB", "LB", "CAM", "CDM"]
    nationalities = ["Brazil", "Spain", "England", "Germany", "Argentina", "France", "Netherlands", "Italy"]

    youth_player = {
        "id": str(uuid.uuid4()),
        "name": random.choice(["Leo", "Mason", "Kai", "Luka", "Jamal", "Ethan"]) + " " +
                random.choice(["Rodriguez", "Khan", "Silva", "Rossi", "Okafor", "Nguyen"]),
        "age": random.randint(15, 18),
        "position": random.choice(positions),
        "nationality": random.choice(nationalities),
        "potential": round(random.uniform(75, 90), 1),
        "attack": random.randint(40, 60),
        "defense": random.randint(40, 60),
        "pace": random.randint(40, 70),
        "passing": random.randint(40, 65),
        "form": 1.0,
        "morale": 1.0
    }

    return youth_player

# === Morale/Form System ===
def update_morale(player):
    """
    Update player's morale and form based on last match performance.
    """
    last_rating = player.get("last_match_rating", 6.0)  # out of 10
    morale = player.get("morale", 1.0)
    form = player.get("form", 1.0)

    # Adjust based on rating
    if last_rating >= 8:
        morale += 0.1
        form += 0.05
    elif last_rating <= 5:
        morale -= 0.1
        form -= 0.05

    # Clamp values
    player["morale"] = round(max(0.5, min(1.5, morale)), 2)
    player["form"] = round(max(0.5, min(1.5, form)), 2)
    player["message"] = f"Updated morale and form after rating {last_rating}"

    return player
