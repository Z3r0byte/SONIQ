# coding=utf-8
import fingerprinting.fourier_transform as fourier
import fingerprinting.peaks as peaks
import fingerprinting.fingerprint as fingerprint
from scipy.io.wavfile import read
import time as t
import sys
import os
import files.filehandler as files
import database.databasehelper as dbhelper

AUDIO_DIR = "Audio Samples/Top 2000"
file_array = files.find_all_files(AUDIO_DIR)
for file in file_array:
    file = file.decode(sys.getfilesystemencoding()).encode("UTF8")  # bug oplossen die MySQL liet crashen door ongeldig karakter (é)
    artist, title = files.artist_title(file)
    song_id = dbhelper.insert_song(file, title, artist)
    if dbhelper.is_fingerprinted(song_id):
        print "Skipping %s..." % title
        continue
    print "Fingerprinting %s by %s..." % (title, artist)
    start_time = t.time()
    dbhelper.remove_fingerprints_for_song(song_id)

    sample_freq, signal = read(os.path.join(AUDIO_DIR, file))
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
