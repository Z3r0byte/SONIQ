# coding=utf-8
import fingerprinting.fourier_transform as fourier
import fingerprinting.peaks as peaks
import fingerprinting.fingerprint as fingerprint
from scipy.io.wavfile import read
import time as t
import files.filehandler as files
import database.databasehelper as dbhelper
import collections

AUDIO_DIR = "Audio Samples/Test set"
files.fingerprint_all(AUDIO_DIR)

print "Matching song...."
start_time = t.time()
sample_freq, signal = read("Audio Samples/Opnames/Testopname-0002.wav")
intensity, freqs, time = fourier.apply_fourier(signal, 1024, sample_freq, 256)
peaks_array = peaks.find_peaks(intensity, 10, 10)
hashes = fingerprint.fingerprint(peaks_array, 200, 20)

fingerprint_data = []
fingerprint_dictionary = {}
for hash in hashes:
    fingerprint_data.append(hash[0])
    fingerprint_dictionary[hash[0]] = hash[1]
fingerprint_match_count = dbhelper.get_songs_with_fingerprints(fingerprint_data)[:1000]

confidences = []
for match in fingerprint_match_count:
    offsets = dbhelper.get_offsets_for_fingerprints_of_song(fingerprint_data, match[0])

    differences = []
    for offset in offsets:
        differences.append(abs(fingerprint_dictionary[str(offset[1]).lower()] - offset[2]))

    diff_freqs = collections.Counter(differences)
    total = 0
    for diff_freq in diff_freqs.values():
        if diff_freq == 1:
            continue
        else:
            total += pow(diff_freq, 2)
    confidences.append([match[0], float(total)/len(offsets)])
confidences.sort(key=lambda x: x[1])
confidences.reverse()
print confidences
matched_song = dbhelper.get_song_by_id(confidences[0][0])
print "    Most probable song is %s by %s with a confidence of %f" % (matched_song[0], matched_song[1], confidences[0][1])
print "    Matched in %f seconds" % (t.time() - start_time)
