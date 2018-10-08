import mysql.connector as mysql

HOST = "localhost"
DATABASE = "SONIQ"
USER = "root"
PASSWORD = "password"

conn = mysql.connect(host=HOST, user=USER, passwd=PASSWORD, database=DATABASE, charset='utf8')
cursor = conn.cursor()


def insert_song(filename, title="", artist=""):
    if get_song_id(filename) is not None:
        return get_song_id(filename)
    query = "INSERT INTO songs (filename, title, artist) VALUES (%s, %s, %s)"  # query met placeholders tegen SQL injectie
    args = (filename, title, artist)  # lijst met argumenten maken voor in de placeholder
    cursor.execute(query, args)  # query uitvoeren
    conn.commit()  # query doorvoeren
    return cursor.lastrowid


def fingerprint_song(song_id):
    query = "UPDATE songs SET fingerprinted = 1 WHERE id = %s"
    args = (song_id,)
    cursor.execute(query, args)
    conn.commit()


def is_fingerprinted(song_id):
    query = "SELECT fingerprinted FROM songs WHERE id = %s"
    args = (song_id,)
    cursor.execute(query, args)
    fingerprinted = cursor.fetchone()
    if fingerprinted[0] == 1:
        return True
    else:
        return False


def remove_fingerprints_for_song(song_id):
    query = "DELETE FROM fingerprints WHERE song_id = %s"
    args = (song_id,)
    cursor.execute(query, args)
    conn.commit()


def get_song_id(filename):
    query = "SELECT id FROM songs WHERE filename = %s"
    args = (filename,)
    cursor.execute(query, args)
    id = cursor.fetchone()
    if id is not None:
        return id[0]
    return None


def insert_hashes(fingerprints):
    query = "INSERT INTO fingerprints (fingerprint, song_id, offset) VALUES (UNHEX(%s), %s, %s)"
    cursor.executemany(query, fingerprints)
    conn.commit()
