from config import SERVER_HOST, SERVER_PORT, SAMPLE_FREQ
from flask import Flask, jsonify, request
import database.databasehelper as dbhelper
import uuid
import files.filehandler as files
import matching.match as match
import numpy as np

app = Flask(__name__)


@app.route("/search/new", methods=["GET"])
def generate_search_id():
    files.cleanup()
    search_id = str(uuid.uuid4())
    files.create_search_file(search_id)
    return jsonify({"search_id": search_id})


@app.route("/songs/<song_id>", methods=["GET"])
def get_songs(song_id):
    if song_id == "all":
        songs = dbhelper.get_all_songs()
    else:
        songs = dbhelper.get_song_by_id(song_id)
    responses = []
    for song in songs:
        responses.append({"song": song[0], "artist": song[1]})
    return jsonify(responses)


@app.route("/search/data", methods=["POST"])
def process_data():
    search_id = request.headers.get("SEARCH_ID")
    if search_id is None:
        return "Geen zoek-id opgegeven", 403
    try:
        uuid.UUID(search_id, version=4)
    except ValueError:
        return "Ongeldig zoek-id", 403
    if not files.search_file_exists(search_id):
        return "Zoekopdracht verlopen of nooit aangevraagd", 403

    file_data = files.read_save_file(search_id)
    if file_data.size >= (SAMPLE_FREQ * 10):
        return "Zoekopdracht te groot", 403
    post_data = request.get_json(force=True)
    audio_array = np.array(post_data['data'], dtype=np.int16)
    total_array = np.append(file_data, audio_array)
    files.save_search_file(search_id, total_array)

    success, confidences, song_id, result, time = match.match(total_array)
    response = {"success": success, "confidence": confidences[0][1], "song_id": song_id, "result": result, "time": time}
    return jsonify(response)


def start():
    print "================================================================================================================================"
    print "| WARNING: Do not make this server externally available! It is not made to be secure and probably isn't. Use at your own risk! |"
    print "================================================================================================================================"
    print
    files.create_temp_folder()
    app.run(host=SERVER_HOST, port=SERVER_PORT)
