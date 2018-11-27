from config import HOST, USER, PASSWORD, DATABASE
import psycopg2

conn = psycopg2.connect(host=HOST, user=USER, password=PASSWORD, dbname=DATABASE)
conn.set_session(autocommit=True)
cursor = conn.cursor()


def insert_song(filename, title="", artist="", conn=conn, cursor=cursor):
    if get_song_id(filename) is not None:
        return get_song_id(filename)
    query = "INSERT INTO songs (filename, title, artist) VALUES (%s, %s, %s)"  # query met placeholders tegen SQL injectie
    args = (filename, title, artist)  # lijst met argumenten maken voor in de placeholder
    cursor.execute(query, args)  # query uitvoeren
    conn.commit()  # query doorvoeren
    return cursor.lastrowid


def fingerprint_song(song_id, conn=conn, cursor=cursor):
    query = "UPDATE songs SET fingerprinted = true WHERE id = %s"
    args = (song_id,)
    cursor.execute(query, args)
    conn.commit()


def is_fingerprinted(song_id, cursor=cursor):
    query = "SELECT fingerprinted FROM songs WHERE id = %s"
    args = (song_id,)
    cursor.execute(query, args)
    fingerprinted = cursor.fetchone()
    if fingerprinted[0] == 1:
        return True
    else:
        return False


def remove_fingerprints_for_song(song_id, conn=conn, cursor=cursor):
    query = "DELETE FROM fingerprints WHERE song_id = %s"
    args = (song_id,)
    cursor.execute(query, args)
    conn.commit()


def get_song_id(filename, cursor=cursor):
    query = "SELECT id FROM songs WHERE filename = %s"
    args = (filename,)
    cursor.execute(query, args)
    id = cursor.fetchone()
    if id is not None:
        return id[0]
    return None


def get_song_by_id(id, cursor=cursor):
    query = "SELECT title, artist FROM songs WHERE id = %s"
    args = (id,)
    cursor.execute(query, args)
    return cursor.fetchall()


def get_all_songs(cursor=cursor):
    query = "SELECT title, artist FROM songs"
    cursor.execute(query)
    return cursor.fetchall()


def insert_hashes(fingerprints, conn=conn, cursor=cursor):
    query = "INSERT INTO fingerprints (fingerprint, song_id, time) VALUES (%s, %s, %s)"
    cursor.executemany(query, fingerprints)
    conn.commit()


def get_songs_with_fingerprints(fingerprints, cursor=cursor):
    placeholder = ",".join(["%s"] * len(fingerprints))  # placeholder strings maken voor in query
    query = "SELECT song_id, COUNT(*) as cnt FROM (SELECT song_id FROM fingerprints WHERE fingerprint IN (%s) GROUP BY song_id,fingerprint) tmp GROUP BY song_id ORDER BY cnt DESC LIMIT 10" % placeholder
    args = tuple(fingerprints)
    cursor.execute(query, args)
    return cursor.fetchall()


def get_times_for_fingerprints_of_song(fingerprints, song_id, cursor=cursor):
    placeholder = ",".join(["%s"] * len(fingerprints))  # placeholder strings maken voor in query
    query = "SELECT song_id, fingerprint, time FROM fingerprints WHERE fingerprint IN (%s) AND song_id = %s GROUP BY song_id,fingerprint,time" % (
    placeholder, song_id)
    args = tuple(fingerprints)
    cursor.execute(query, args)
    return cursor.fetchall()
