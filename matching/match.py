from config import SAMPLE_FREQ, NFFT_WINDOW, N_OVERLAP, PEAK_TIME_WINDOW, PEAK_FREQ_WINDOW, FINGERPRINT_TIME_WINDOW, MIN_CONFIDENCE_FOR_STOP
import fingerprinting.fourier_transform as fourier
import fingerprinting.peaks as peaks
import fingerprinting.fingerprint as fingerprint
from scipy.io.wavfile import read
import time as t
import database.databasehelper as dbhelper
import collections


def match(signal, cursor=None):
    start_time = t.time()
    intensity, freqs, time = fourier.apply_fourier(signal, NFFT_WINDOW, SAMPLE_FREQ, N_OVERLAP)
    peaks_array = peaks.find_peaks(intensity, PEAK_TIME_WINDOW, PEAK_FREQ_WINDOW)
    hashes = fingerprint.fingerprint(peaks_array, FINGERPRINT_TIME_WINDOW)

    if len(hashes) == 0:
        return False, 0, 0, "Unable to generate hashes. Not enough peaks? No match.", (t.time() - start_time)

    fingerprint_data = []
    fingerprint_dictionary = {}
    for hash in hashes:
        fingerprint_data.append(hash[0])
        fingerprint_dictionary[hash[0]] = hash[1]
    if cursor is not None:
        fingerprint_match_count = dbhelper.get_songs_with_fingerprints(fingerprint_data, cursor)
    else:
        fingerprint_match_count = dbhelper.get_songs_with_fingerprints(fingerprint_data)

    if len(fingerprint_match_count) == 0:
        return False, 0, 0, "Did not find any similarities in database. No match.", (t.time() - start_time)

    confidences = []
    for match in fingerprint_match_count:
        if cursor is not None:
            offsets = dbhelper.get_times_for_fingerprints_of_song(fingerprint_data, match[0], cursor)
        else:
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
        confidence = [match[0], float(total) / len(offsets)]
        confidences.append(confidence)
        if confidence[1] >= MIN_CONFIDENCE_FOR_STOP:
            break
    confidences.sort(key=lambda x: x[1])
    confidences.reverse()
    if cursor is not None:
        matched_song = dbhelper.get_song_by_id(confidences[0][0], cursor)[0]
    else:
        matched_song = dbhelper.get_song_by_id(confidences[0][0])[0]

    if len(confidences) == 1:
        return True, confidences, confidences[0][0], "Most probable song is %s by %s with a confidence of %f" % (matched_song[0], matched_song[1], confidences[0][1]), (t.time() - start_time)
    elif confidences[0][1] > (2 * confidences[1][1]):
        return True, confidences, confidences[0][0], "Most probable song is %s by %s with a confidence of %f" % (matched_song[0], matched_song[1], confidences[0][1]), (t.time() - start_time)
    else:
        return False, confidences, confidences[0][0], "Unable to get reliable match. Best guess is %s by %s with a confidence of %f" % (matched_song[0], matched_song[1], confidences[0][1]), (t.time() - start_time)


def match_file(path):
    """
    Matcht een bestand aan de origineel in de database
    :rtype: bool, array([int, float]), int, string, float
    :return: Match, confidences, song id, resultaat, tijd
    :param path: Path to the file te match
    """
    sample_freq, signal = read(path)
    if sample_freq != SAMPLE_FREQ:
        print "########################################################################################################"
        print "Warning! Sample frequency is not the same as the config value. There probably won't be a reliable match!"
        print "########################################################################################################"
    return match(signal)
