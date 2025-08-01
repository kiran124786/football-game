# backend/firebase_service.py

import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase only once
cred = credentials.Certificate("firebase-key.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

# === Save a match result ===
def save_match_result(user_id, match_result):
    db.collection("users").document(user_id).collection("matches").add(match_result)
    return {"message": "Match result saved"}

# === Save or update player ===
def save_player(user_id, player_data):
    player_id = player_data.get("id")
    if player_id:
        db.collection("users").document(user_id).collection("players").document(player_id).set(player_data)
        return {"message": "Player saved", "id": player_id}
    return {"error": "Player ID missing"}

# === Get all players of user ===
def get_players(user_id):
    players_ref = db.collection("users").document(user_id).collection("players")
    docs = players_ref.stream()
    return [doc.to_dict() for doc in docs]

# === Save transfer history ===
def log_transfer(user_id, transfer_data):
    db.collection("users").document(user_id).collection("transfers").add(transfer_data)
    return {"message": "Transfer logged"}

# === Save training history ===
def log_training(user_id, training_data):
    db.collection("users").document(user_id).collection("training").add(training_data)
    return {"message": "Training logged"}
