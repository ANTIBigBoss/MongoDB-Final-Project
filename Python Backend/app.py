from flask import Flask, request, jsonify
from pymongo import MongoClient
from datetime import datetime

app = Flask(__name__)

client = MongoClient("mongodb://localhost:27017/?replicaSet=rs1")
db = client["FinalAssignment"]
players_collection = db["players"]

@app.route('/players', methods=['POST'])
def create_player():
    data = request.get_json()
    data['created_at'] = datetime.utcnow()
    result = players_collection.insert_one(data)
    return jsonify({
        "message": "Player created successfully",
        "player_id": data.get("player_id"),
        "inserted_id": str(result.inserted_id)
    }), 201

@app.route('/players', methods=['GET'])
def get_players():
    players = list(players_collection.find({}, {"_id": 0}))
    return jsonify(players), 200

@app.route('/players/<player_id>', methods=['GET'])
def get_player_by_id(player_id):
    player = players_collection.find_one({"player_id": player_id}, {"_id": 0})
    if player:
        return jsonify(player), 200
    return jsonify({"error": "Player not found"}), 404


@app.route('/players/<player_id>', methods=['PUT'])
def update_player(player_id):
    data = request.get_json()
    result = players_collection.update_one({"player_id": player_id}, {"$set": data})
    if result.matched_count:
        return jsonify({"message": "Player updated successfully", "player_id": player_id}), 200
    return jsonify({"error": "Player not found"}), 404

@app.route('/players/<player_id>', methods=['DELETE'])
def delete_player(player_id):
    result = players_collection.delete_one({"player_id": player_id})
    if result.deleted_count:
        return jsonify({"message": "Player deleted successfully", "player_id": player_id}), 200
    return jsonify({"error": "Player not found"}), 404

if __name__ == '__main__':
    app.run(debug=True, port=5000)
