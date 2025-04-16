from flask import Flask
from flask_restx import Api, Resource, fields
from pymongo import MongoClient
from datetime import datetime

app = Flask(__name__)
api = Api(app, version="1.0", title="Player API", description="API for managing player records")

ns = api.namespace("players", description="Player operations")

client = MongoClient("mongodb://localhost:27017/?replicaSet=rs1")
db = client["FinalAssignment"]
players_col = db["players"]

player_model = api.model("Player", {
    "player_id": fields.String(required=True, description="Player identifier"),
    "username": fields.String(required=True, description="Username"),
    "profile": fields.String(description="Player profile"),
    "stats": fields.Raw(description="Player statistics"),
    "login_info": fields.Raw(description="Login information"),
    "hardware_info": fields.Raw(description="Hardware info"),
    "created_at": fields.String(description="Creation timestamp"),
    "animal_rank": fields.String(description="Animal rank")
})

@ns.route("/")
class PlayerList(Resource):
    @ns.doc("list_players")
    @ns.marshal_list_with(player_model)
    def get(self):
        players = list(players_col.find({}, {"_id": 0}))
        for p in players:
            if "created_at" in p and isinstance(p["created_at"], datetime):
                p["created_at"] = p["created_at"].isoformat()
        return players

    @ns.doc("create_player")
    @ns.expect(player_model)
    def post(self):
        data = api.payload
        data["created_at"] = datetime.utcnow().isoformat()
        result = players_col.insert_one(data)
        return {"message": "Player created successfully", "player_id": data.get("player_id"), "inserted_id": str(result.inserted_id)}, 201

@ns.route("/<string:player_id>")
@ns.response(404, "Player not found")
@ns.param("player_id", "The player identifier")
class Player(Resource):
    @ns.doc("get_player")
    @ns.marshal_with(player_model)
    def get(self, player_id):
        """Fetch a given player"""
        player = players_col.find_one({"player_id": player_id}, {"_id": 0})
        if not player:
            api.abort(404, "Player not found")
        if "created_at" in player and isinstance(player["created_at"], datetime):
            player["created_at"] = player["created_at"].isoformat()
        return player

    @ns.doc("update_player")
    @ns.expect(player_model)
    def put(self, player_id):
        data = api.payload
        result = players_col.update_one({"player_id": player_id}, {"$set": data})
        if result.matched_count == 0:
            api.abort(404, "Player not found")
        return {"message": "Player updated successfully", "player_id": player_id}

    @ns.doc("delete_player")
    def delete(self, player_id):
        result = players_col.delete_one({"player_id": player_id})
        if result.deleted_count == 0:
            api.abort(404, "Player not found")
        return {"message": "Player deleted successfully", "player_id": player_id}

if __name__ == '__main__':
    app.run(debug=True, port=5000)
