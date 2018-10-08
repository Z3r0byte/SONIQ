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
import binascii as bin

AUDIO_DIR = "Audio Samples/Top 2000"
# files.fingerprint_all(AUDIO_DIR)

print "Matching song...."
start_time = t.time()
sample_freq, signal = read("Audio Samples/Opnames/Testopname-0087.wav")
intensity, freqs, time = fourier.apply_fourier(signal, 1024, sample_freq, 256)
peaks_array = peaks.find_peaks(intensity, 5, 5)
print len(peaks_array)
hashes = fingerprint.fingerprint(peaks_array, 20, 10)

fingerprint_data = []
for hash in hashes:
    data = hash[0]
    fingerprint_data.append(data)
print dbhelper.get_songs_with_fingerprints(fingerprint_data)[:1000]
print "    Matched in %f seconds" % (t.time() - start_time)
