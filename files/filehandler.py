# coding=utf-8
import os
import re
import sys
import database.databasehelper as dbhelper
import fingerprinting.fourier_transform as fourier
import fingerprinting.peaks as peaks
import fingerprinting.fingerprint as fingerprint
from scipy.io.wavfile import read
import time as t


def fingerprint_all(AUDIO_DIR):
    file_array = find_all_files(AUDIO_DIR)
    for file in file_array:
        path = file
        file = file.decode(sys.getfilesystemencoding()).encode(
            "UTF8")  # bug oplossen die MySQL liet crashen door ongeldig karakter (é)
        artist, title = artist_title(file)
        song_id = dbhelper.insert_song(file, title, artist)
        if dbhelper.is_fingerprinted(song_id):
            print "Skipping %s..." % title
            continue
        print "Fingerprinting %s by %s..." % (title, artist)
        start_time = t.time()
        dbhelper.remove_fingerprints_for_song(song_id)

        sample_freq, signal = read(os.path.join(AUDIO_DIR, path))
        intensity, freqs, time = fourier.apply_fourier(signal, 1024, sample_freq, 256)
        peaks_array = peaks.find_peaks(intensity, 5, 5)
        hashes = fingerprint.fingerprint(peaks_array, 20, 10)

        fingerprint_data = []
        for hash in hashes:
            data = (hash[0], song_id, hash[1])
            fingerprint_data.append(data)
        dbhelper.insert_hashes(fingerprint_data)
        dbhelper.fingerprint_song(song_id)
        print "    Fingerprinted in %d seconds" % (t.time() - start_time)


def find_all_files(dir):
    """
    :returns: lijst met WAVE bestanden in een bepaalde map
    :param dir: de map waarin gezocht moet worden
    :return: een 1D array met de namen van de bestanden
    """
    filenames = []
    for file in os.listdir(dir):
        if file.endswith(".wav"):  # SONIQ ondersteunt alleen WAVE bestanden
            filenames.append(file)
    return filenames


def artist_title(filename):
    """
    :returns: de titel van het lied en de naam van de artiest indien mogelijk
    :param filename: bestandsnaam
    :return: artiestnaam (string), titel (string)
    """
    filename = filename[:-4]
    if re.search("([0-9]{4} )", filename, flags=0) is not None:
        filename = filename[5:]
    dash_index = filename.find('-')
    if dash_index is -1:
        return "", filename
    return filename[:dash_index - 1], filename[dash_index + 2:]
