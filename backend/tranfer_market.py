# backend/transfer_market.py

import uuid
import random

# Dummy transfer list (in-memory for now)
TRANSFER_LIST = []

POSITIONS = ["GK", "CB", "LB", "RB", "CDM", "CM", "CAM", "LM", "RM", "ST"]
NATIONALITIES = ["Spain", "Germany", "Brazil", "England", "Argentina", "Italy", "France"]

def generate_transfer_list(n=10):
    """
    Create a list of players available for transfer.
    """
    global TRANSFER_LIST
    TRANSFER_LIST = []

    for _ in range(n):
        player = {
            "id": str(uuid.uuid4()),
            "name": random.choice(["Kai", "Luka", "Noah", "Leo", "Oscar", "Rami"]) + " " +
                    random.choice(["Silva", "Rossi", "Khan", "Nguyen", "Lopez"]),
            "age": random.randint(18, 30),
            "position": random.choice(POSITIONS),
            "nationality": random.choice(NATIONALITIES),
            "attack": random.randint(50, 90),
            "defense": random.randint(50, 90),
            "pace": random.randint(50, 90),
            "passing": random.randint(50, 90),
            "rating": round(random.uniform(65, 88), 1),
            "price": random.randint(3_000_000, 15_000_000),
            "form": round(random.uniform(0.8, 1.2), 2),
            "morale": round(random.uniform(0.8, 1.2), 2),
            "team": "Free Agent"
        }
        TRANSFER_LIST.append(player)

    return TRANSFER_LIST

def get_transfer_list(position_filter=None, max_price=None):
    """
    Get players on the transfer market, with optional filters.
    """
    filtered = TRANSFER_LIST
    if position_filter:
        filtered = [p for p in filtered if p["position"] == position_filter]
    if max_price:
        filtered = [p for p in filtered if p["price"] <= max_price]
    return filtered

def buy_player(player_id, buying_team, budget):
    """
    Simulate buying a player if budget allows.
    """
    for player in TRANSFER_LIST:
        if player["id"] == player_id:
            if budget >= player["price"]:
                player["team"] = buying_team
                TRANSFER_LIST.remove(player)
                return {
                    "success": True,
                    "message": f"{player['name']} successfully signed by {buying_team}",
                    "remaining_budget": budget - player["price"],
                    "player": player
                }
            else:
                return {
                    "success": False,
                    "message": "Not enough budget to buy this player.",
                    "required": player["price"],
                    "your_budget": budget
                }
    return {"success": False, "message": "Player not found in transfer list."}
