# backend/app.py
from flask import Flask, request, jsonify
from match_simulator import simulate_match
from training_model import train_player
from player_manager import transfer_player, generate_youth_player, update_morale

app = Flask(__name__)

@app.route("/")
def home():
    return "AI Football Club Manager Backend Running"

@app.route("/simulate_match", methods=["POST"])
def simulate():
    data = request.json
    result = simulate_match(data["team_a"], data["team_b"])
    return jsonify(result)

@app.route("/train_player", methods=["POST"])
def train():
    data = request.json
    result = train_player(data["player"])
    return jsonify(result)

@app.route("/transfer_player", methods=["POST"])
def transfer():
    data = request.json
    result = transfer_player(data["player_id"], data["from_team"], data["to_team"])
    return jsonify(result)

@app.route("/generate_youth", methods=["GET"])
def generate_youth():
    player = generate_youth_player()
    return jsonify(player)

@app.route("/update_morale", methods=["POST"])
def morale():
    data = request.json
    updated = update_morale(data["player"])
    return jsonify(updated)

if __name__ == "__main__":
    app.run(debug=True)
