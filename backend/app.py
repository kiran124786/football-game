# backend/app.py

from flask import Flask, request, jsonify

# Core Features
from match_simulator import simulate_match
from training_model import train_player
from player_manager import transfer_player, generate_youth_player, update_morale

# Transfer Market
from transfer_market import generate_transfer_list, get_transfer_list, buy_player

# Firebase DB
from firebase_service import (
    save_match_result, save_player, get_players, log_transfer, log_training
)

# League & Fixtures
from league_system import initialize_league, update_league_table, get_league_table
from schedule_generator import generate_fixtures, shuffle_fixtures, get_fixtures_by_round

# TheSportsDB API Integration
from api_thesportsdb import (
    search_team, search_player, get_teams_in_league,
    get_next_events, get_last_results
)

# Flask app
app = Flask(__name__)
LEAGUE_SCHEDULE = []

@app.route("/")
def home():
    return "⚽ AI Football Club Manager Backend Running"

# === Match Simulation ===
@app.route("/simulate_match", methods=["POST"])
def simulate():
    data = request.json
    result = simulate_match(data["team_a"], data["team_b"])
    return jsonify(result)

# === Training ===
@app.route("/train_player", methods=["POST"])
def train():
    data = request.json
    player = train_player(data["player"])
    log_training(data["user_id"], player)
    return jsonify(player)

# === Transfer Player (Direct) ===
@app.route("/transfer_player", methods=["POST"])
def transfer():
    data = request.json
    result = transfer_player(data["player_id"], data["from_team"], data["to_team"])
    log_transfer(data["user_id"], result)
    return jsonify(result)

# === Youth Academy ===
@app.route("/generate_youth", methods=["GET"])
def generate_youth():
    player = generate_youth_player()
    return jsonify(player)

# === Morale/Form Update ===
@app.route("/update_morale", methods=["POST"])
def morale():
    data = request.json
    updated = update_morale(data["player"])
    return jsonify(updated)

# === Transfer Market APIs ===
@app.route("/transfer_market/generate", methods=["GET"])
def market_generate():
    players = generate_transfer_list(n=15)
    return jsonify(players)

@app.route("/transfer_market", methods=["GET"])
def market_list():
    position = request.args.get("position")
    max_price = request.args.get("max_price", type=int)
    players = get_transfer_list(position_filter=position, max_price=max_price)
    return jsonify(players)

@app.route("/transfer_market/buy", methods=["POST"])
def market_buy():
    data = request.json
    result = buy_player(data["player_id"], data["buying_team"], data["budget"])
    if result["success"]:
        log_transfer(data["user_id"], result)
    return jsonify(result)

# === Firebase Player APIs ===
@app.route("/players/<user_id>", methods=["GET"])
def list_players(user_id):
    return jsonify(get_players(user_id))

@app.route("/players/<user_id>/save", methods=["POST"])
def save_user_player(user_id):
    player = request.json
    return jsonify(save_player(user_id, player))

@app.route("/matches/<user_id>/save", methods=["POST"])
def save_match(user_id):
    result = request.json
    return jsonify(save_match_result(user_id, result))

# === League System ===
@app.route("/league/init", methods=["POST"])
def init_league():
    teams = request.json["teams"]
    return jsonify(initialize_league(teams))

@app.route("/league/update", methods=["POST"])
def league_update():
    data = request.json
    return jsonify(update_league_table(
        data["team_a"], data["team_b"], data["score_a"], data["score_b"]
    ))

@app.route("/league/table", methods=["GET"])
def league_table():
    return jsonify(get_league_table())

# === Schedule Generator ===
@app.route("/schedule/init", methods=["POST"])
def init_schedule():
    global LEAGUE_SCHEDULE
    teams = request.json["teams"]
    LEAGUE_SCHEDULE = shuffle_fixtures(generate_fixtures(teams))
    return jsonify({
        "message": "Schedule generated",
        "rounds": len(LEAGUE_SCHEDULE)
    })

@app.route("/schedule/<int:matchday>", methods=["GET"])
def get_schedule(matchday):
    global LEAGUE_SCHEDULE
    return jsonify(get_fixtures_by_round(LEAGUE_SCHEDULE, matchday))

# === TheSportsDB API Routes ===
@app.route("/thesportsdb/team", methods=["GET"])
def team_info():
    team_name = request.args.get("name")
    return jsonify(search_team(team_name))

@app.route("/thesportsdb/player", methods=["GET"])
def player_info():
    player_name = request.args.get("name")
    return jsonify(search_player(player_name))

@app.route("/thesportsdb/league_teams", methods=["GET"])
def league_teams():
    league_name = request.args.get("league")
    return jsonify(get_teams_in_league(league_name))

@app.route("/thesportsdb/team/next", methods=["GET"])
def next_events():
    team_id = request.args.get("id")
    return jsonify(get_next_events(team_id))

@app.route("/thesportsdb/team/last", methods=["GET"])
def last_results():
    team_id = request.args.get("id")
    return jsonify(get_last_results(team_id))

# === Run Server ===
if __name__ == "__main__":
    app.run(debug=True)
