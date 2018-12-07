from __future__ import print_function
import files.filehandler as file
import matching.match as match
import os
import math


def run_tests(sample_dir):
    """
    Test alle bestanden in de opgegeven map en berekent gemiddeldes, percentages, etc. van de matches
    :param sample_dir: Bestandspad naar de map met fragmenten om te testen
    """
    print("Preparing tests")
    sample_files = file.find_all_files(sample_dir)
    total_files = len(sample_files)
    progress = 0
    results = []  # [[success, correct, filename, time, confidence, found_id],...]
    for sample_file in sample_files:
        progress += 1
        print("\rRunning tests (%d/%d)..." % (progress, total_files), end="")
        sample_file_path = os.path.join(sample_dir, sample_file)
        is_valid, song_id = file.get_song_id_from_filename(sample_file)
        if not is_valid:
            print("File %s doesn't have a valid filename, skipping" % sample_file)
            continue
        if song_id == 0:
            continue
        success, confidences, found_song_id, result, time, title, artist = match.match_file(sample_file_path)
        correct = song_id == found_song_id or (not success and song_id == 0)
        results.append([success, correct, sample_file, time, confidences[0][1], found_song_id])
    total_results = 0
    total_successful_results = 0
    total_correct_results = 0
    total_correct_successful_results = 0
    total_time = 0
    times = []
    for result in results:
        total_results += 1
        total_time += result[3]
        times.append(result[3])
        if not result[0]:
            if result[1]:
                print("Could not find %s in the database in %fs, as expected" % (result[2], result[3]))
                total_correct_results += 1
            else:
                print("File %s could not be matched in %fs" % (result[2], result[3]))
        else:
            total_successful_results += 1
            if result[1]:
                print("File %s was correctly matched with a confidence of %f in %fs" % (result[2], result[4], result[3]))
                total_correct_results += 1
                total_correct_successful_results += 1
            else:
                print("File %s was incorrectly matched with a confidence of %f in %fs. (found %d)" % (result[2], result[4], result[3], result[5]))
    print("========================================================================")
    print(" Tests run: %d" % total_results)
    print(" Tests successful: %d" % total_successful_results)
    print(" Tests correct: %d" % total_correct_results)
    print("------------------------------------------------------------------------")
    print(" Average time: %fs" % (total_time/total_results))
    print(" 90-percentile: %fs" % get_90_percentile(times))
    print(" Percentage correct of successful: %f" % ((float(total_correct_successful_results)/total_successful_results)*100))
    print(" Percentage correct of total: %f" % ((float(total_correct_results)/total_results)*100))
    print("========================================================================")


def get_90_percentile(times):
    """
    Berekent onder welk getal minimaal 90% van de getallen in de opgegeven array ligt
    :param times: array met getallen
    :return: Het getal waaronder 90% van de getallen ligt
    """
    times.sort()
    length = len(times)
    last_5_percent = int(math.ceil(length * 0.90))
    return times[last_5_percent - 1]
