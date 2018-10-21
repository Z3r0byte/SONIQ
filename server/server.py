from config import SERVER_HOST, SERVER_PORT
from flask import Flask, jsonify, request
import database.databasehelper as dbhelper
import uuid

app = Flask(__name__)


@app.route("/search/new", methods=["GET"])
def generate_search_id():
    return jsonify({"search_id": str(uuid.uuid4())})


@app.route("/songs/<song_id>", methods=["GET"])
def get_songs(song_id):
    if song_id == "all":
        songs = dbhelper.get_all_songs()
    else:
        songs = dbhelper.get_song_by_id(song_id)
    return jsonify(songs)


@app.route("/search/data", methods=["POST"])
def process_data():
    search_id = request.headers.get("SEARCH_ID")
    if search_id is None:
        return "Geen zoek-id opgegeven", 403
    try:
        uuid.UUID(search_id, version=4)
    except ValueError:
        return "Ongeldig zoek-id", 403
    return search_id


def start():
    print "================================================================================================================================"
    print "| WARNING: Do not make this server externally available! It is not made to be secure and probably isn't. Use at your own risk! |"
    print "================================================================================================================================"
    print
    app.run(host=SERVER_HOST, port=SERVER_PORT)
