# coding=utf-8
from config import AUDIO_DIR, SAMPLE_FREQ, NFFT_WINDOW, N_OVERLAP, PEAK_FREQ_WINDOW, PEAK_TIME_WINDOW, FINGERPRINT_TIME_WINDOW, MIN_CONFIDENCE_FOR_STOP
import fingerprinting.fourier_transform as fourier
import fingerprinting.peaks as peaks
import fingerprinting.fingerprint as fingerprint
from scipy.io.wavfile import read
import time as t
import files.filehandler as files
import database.databasehelper as dbhelper
import collections

files.fingerprint_all(AUDIO_DIR)

print "Matching song...."
start_time = t.time()
sample_freq, signal = read("Audio Samples/Opnames/Testopname-0000-0.wav")
if sample_freq != SAMPLE_FREQ:
    print "########################################################################################################"
    print "Warning! Sample frequency is not the same as the config value. There probably won't be a reliable match!"
    print "########################################################################################################"
intensity, freqs, time = fourier.apply_fourier(signal, NFFT_WINDOW, SAMPLE_FREQ, N_OVERLAP)
peaks_array = peaks.find_peaks(intensity, PEAK_TIME_WINDOW, PEAK_FREQ_WINDOW)
hashes = fingerprint.fingerprint(peaks_array, FINGERPRINT_TIME_WINDOW)

if len(hashes) == 0:
    print "    Unable to generate hashes. Not enough peaks? No match."
    exit()

fingerprint_data = []
fingerprint_dictionary = {}
for hash in hashes:
    fingerprint_data.append(hash[0])
    fingerprint_dictionary[hash[0]] = hash[1]
fingerprint_match_count = dbhelper.get_songs_with_fingerprints(fingerprint_data)  # alleen de eerste honderd om tijd te besparen. Er is namelijk een grote kans dat het juiste lied ook een van de meeste overeenkomsten zal hebben

if len(fingerprint_match_count) == 0:
    print "    Did not find any similarities in database. No match."
    exit()

confidences = []
for match in fingerprint_match_count:
    offsets = dbhelper.get_times_for_fingerprints_of_song(fingerprint_data, match[0])

    differences = []
    for offset in offsets:
        differences.append(round(fingerprint_dictionary[str(offset[1]).lower()] - offset[2], -1))

    diff_freqs = collections.Counter(differences)
    total = 0
    for diff_freq in diff_freqs.values():
        if diff_freq == 1:
            continue
        else:
            total += pow(diff_freq, 2)
    confidence = [match[0], float(total)/len(offsets)]
    confidences.append(confidence)
    if confidence[1] >= MIN_CONFIDENCE_FOR_STOP:
        break
confidences.sort(key=lambda x: x[1])
confidences.reverse()
print confidences
matched_song = dbhelper.get_song_by_id(confidences[0][0])

if len(confidences) == 1:
    print "    Most probable song is %s by %s with a confidence of %f" % (matched_song[0], matched_song[1], confidences[0][1])
elif confidences[0][1] > (2 * confidences[1][1]):
    print "    Most probable song is %s by %s with a confidence of %f" % (matched_song[0], matched_song[1], confidences[0][1])
else:
    print "    Unable to get reliable match. Best guess is %s by %s with a confidence of %f" % (matched_song[0], matched_song[1], confidences[0][1])
print "    Matched in %f seconds" % (t.time() - start_time)
