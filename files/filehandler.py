# coding=utf-8
from config import SAMPLE_FREQ, NFFT_WINDOW, N_OVERLAP, PEAK_FREQ_WINDOW, PEAK_TIME_WINDOW, FINGERPRINT_TIME_WINDOW
import os
import re
import sys
import database.databasehelper as dbhelper
import fingerprinting.fourier_transform as fourier
import fingerprinting.peaks as peaks
import fingerprinting.fingerprint as fingerprint
from scipy.io.wavfile import read
import time as t
import numpy as np


def fingerprint_all(AUDIO_DIR):
    """
    Maakt vingerafdrukken van alle WAVE bestanden in de opgegeven map in zet voegt deze toe aan de database indien deze nog niet erin staan.
    :param AUDIO_DIR: Het pad naar de map met audiobestanden
    """
    file_array = find_all_files(AUDIO_DIR)
    for file in file_array:
        path = file
        file = file.decode(sys.getfilesystemencoding()).encode(
            "UTF8")  # bug oplossen die MySQL liet crashen door ongeldig karakter (é)
        artist, title = artist_title(file)
        song_id = dbhelper.insert_song(file, title, artist)
        if dbhelper.is_fingerprinted(song_id):
            print "%s is already in our database, skipping..." % title
            continue
        print "Fingerprinting %s by %s..." % (title, artist)
        start_time = t.time()
        dbhelper.remove_fingerprints_for_song(song_id)

        sample_freq, signal = read(os.path.join(AUDIO_DIR, path))
        if sample_freq != SAMPLE_FREQ:
            print "    WARNING: sample frequency is not the same as the one in config, skipping..."
            continue
        intensity, freqs, time = fourier.apply_fourier(signal, NFFT_WINDOW, SAMPLE_FREQ, N_OVERLAP)
        peaks_array = peaks.find_peaks(intensity, PEAK_TIME_WINDOW, PEAK_FREQ_WINDOW)
        hashes = fingerprint.fingerprint(peaks_array, FINGERPRINT_TIME_WINDOW)

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


def get_song_id_from_filename(filename):
    """
    Bepaald het 4-cijferige id van het nummer uit de bestandsnaam. Indien er geen geldig id in de bestandsnaam zit, is succes False en id 0.
    :rtype: bool, int
    :param filename: De bestandsnaam met het song-id.
    :return: succes (bool), id (int)
    """
    if re.search("([0-9]{4})", filename, flags=0) is not None:
        return True, int(re.search("([0-9]{4})", filename, flags=0).group(0))
    else:
        return False, 0


def create_temp_folder():
    if not os.path.isdir("temp"):
        os.mkdir("temp")


def create_search_file(search_id):
    np.save("temp/%s" % search_id, None)


def search_file_exists(search_id):
    return os.path.isfile("temp/%s.npy" % search_id)


def save_search_file(search_id, array):
    np.save("temp/%s" % search_id, array)


def read_save_file(search_id):
    return np.load("temp/%s.npy" % search_id)
