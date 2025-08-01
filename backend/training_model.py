# backend/training_model.py

import random

def train_player(player):
    """
    Simulate training and return updated player stats using a simple rule-based ML-like approach.
    In real case, you'd use a model trained on real datasets.
    """
    # Extract player base stats
    attack = player.get("attack", 50)
    defense = player.get("defense", 50)
    pace = player.get("pace", 50)
    passing = player.get("passing", 50)
    age = player.get("age", 20)
    training_type = player.get("training_type", "balanced")  # Options: attack, defense, pace, balanced

    # Age impact
    age_factor = max(0.8, 1.1 - (age - 18) * 0.03)

    # Improvement logic
    improvement = {
        "attack": random.uniform(0.5, 2.0),
        "defense": random.uniform(0.5, 2.0),
        "pace": random.uniform(0.5, 2.0),
        "passing": random.uniform(0.5, 2.0),
    }

    # Training type boost
    if training_type == "attack":
        improvement["attack"] *= 1.5
    elif training_type == "defense":
        improvement["defense"] *= 1.5
    elif training_type == "pace":
        improvement["pace"] *= 1.5
    elif training_type == "passing":
        improvement["passing"] *= 1.5

    # Apply age factor
    for skill in improvement:
        improvement[skill] *= age_factor

    # Update stats
    player["attack"] = round(attack + improvement["attack"], 1)
    player["defense"] = round(defense + improvement["defense"], 1)
    player["pace"] = round(pace + improvement["pace"], 1)
    player["passing"] = round(passing + improvement["passing"], 1)

    player["message"] = f"Player trained in {training_type}. Improvements applied based on age {age}."

    return player
