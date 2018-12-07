# coding=utf-8
from config import SERVER_HOST, SERVER_PORT, SAMPLE_FREQ, HOST, DATABASE, USER, PASSWORD
from flask import Flask, jsonify, request
from flaskext.mysql import MySQL
import database.databasehelper as dbhelper
import uuid
import files.filehandler as files
import matching.match as match
import numpy as np

app = Flask(__name__)

# Voorbreiden database verbinding
mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = USER
app.config['MYSQL_DATABASE_PASSWORD'] = PASSWORD
app.config['MYSQL_DATABASE_DB'] = DATABASE
app.config['MYSQL_DATABASE_HOST'] = HOST
mysql.init_app(app)


@app.route("/search/new", methods=["GET"])
def generate_search_id():
    """
    Nieuwe zoekopdracht aanmaken en id terugsturen
    :return:
    """
    files.cleanup()
    search_id = str(uuid.uuid4())
    files.create_search_file(search_id)
    return jsonify({"search_id": search_id})


@app.route("/songs/<song_id>", methods=["GET"])
def get_songs(song_id):
    """
    Titel en artiest geven van een liedje
    :param song_id: het id van het liedje, stuurt de informatie terug van alle liedjes indien dit "all" is
    :return:
    """
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
    """
    Verwerkt geüploade data
    :return:
    """
    search_id = request.headers.get("SEARCH_ID")
    print "Processing request " + search_id + "..."
    # Controleren search_id
    if search_id is None:
        return "{ \"error\" : \"Geen zoek-id opgegeven\"}", 403
    try:
        uuid.UUID(search_id, version=4)
    except ValueError:
        return "{ \"error\" : \"Ongeldig zoek-id\"}", 403
    if not files.search_file_exists(search_id):
        return "{ \"error\" : \"Zoekopdracht verlopen of nooit aangevraagd\"}", 403

    # Geüploade data toevoegen aan al ontvangen data
    file_data = files.read_save_file(search_id)
    if file_data.size > (SAMPLE_FREQ * 10):
        return "{ \"error\" : \"Zoekopdracht te groot\"}", 403
    post_data = request.get_json(force=True)
    audio_array = np.array(post_data['data'], dtype=np.int16)
    total_array = np.append(file_data, audio_array)
    files.save_search_file(search_id, total_array)

    # Totaal ontvangen opname matchen en antwoord terug sturen
    success, confidences, song_id, result, time, title, artist = match.match(total_array, mysql.get_db().cursor())
    response = {"success": success, "confidence": confidences[0][1], "song_id": song_id, "result": result,
                "time": time, "song": {"title": title, "artist": artist}}
    return jsonify(response)


@app.errorhandler(505)
def internal_server_error(e):
    """
    Handelt eventuele fouten netjes af met een 500 error code
    :param e:
    :return:
    """
    return "{\"error\": \"Er is een fout opgetreden tijdens het verwerken van je verzoek\"}", 500


def start():
    print "================================================================================================================================"
    print "| WARNING: Do not make this server externally available! It is not made to be secure and probably isn't. Use at your own risk! |"
    print "================================================================================================================================"
    print
    files.create_temp_folder()
    app.run(host=SERVER_HOST, port=SERVER_PORT)
