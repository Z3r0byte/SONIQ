# coding=utf-8
from __future__ import print_function
import numpy as np
import random
import os
import sys
import files.filehandler as file
import database.databasehelper as dbhelper
import matching.match as match
from scipy.io.wavfile import write, read
from config import SAMPLE_FREQ, NOISE_SOURCE_FILE, NOISE_DESTINATION_FOLDER, AUDIO_DIR


def add_noise(input, noise, length, wanted_ratio):
    """
    Voegt ruis toe aan een geluidsfragment
    :param input: Het ruisloze geluid
    :param noise: De ruis (kan bijvoorbeeld een ander geluidsfragment zijn)
    :param length: De lengte van het te genereren fragment, dient minimaal even lang te zijn als de input en/of ruis
    :param wanted_ratio: De gewenste signaal-ruisverhouding
    :return: Een geluidsfragment bestaande uit (een deel van) :param input en :param noise, waarbij :param noise
        is vermenigvuldigd met een factor die zo gekozen is dat de gewenste SNR behaald wordt.
    """
    length = SAMPLE_FREQ * length
    if length >= len(noise) or length >= len(input):
        raise ValueError("De gedefineerde lengte kan niet langer zijn dan (één van) de audiofragmenten")

    start = random.randint(0, (len(input) - length - 1))
    end = start + length
    input = input[start:end]

    start = random.randint(0, (len(noise) - length - 1))
    end = start + length
    noise = noise[start:end]

    input_abs = np.abs(input)
    noise_abs = np.abs(noise)

    ratio = np.average(noise_abs) / np.average(input_abs)
    wanted_ratio = pow(10, -(wanted_ratio / float(10)))
    multiplication_factor = wanted_ratio / ratio
    noise = noise * multiplication_factor
    noise = np.asarray(noise, np.int16)
    output = np.add(noise, input)

    return output


def create_with_noise(amount):
    """
    Genereert een bepaald aantal bestanden met ruis in NOISE_DESTINATION_FOLDER uit AUDIO_DIR met als ruis NOISE_SOURCE_FILE
    :param amount: het aantal te genereren bestanden
    """
    print("Preparing generation of test files")
    sample_files = file.find_all_files(AUDIO_DIR)
    sample_files = random.sample(sample_files, int(amount))
    total_files = len(sample_files)

    progress = 0
    sample_freq, noise = read(NOISE_SOURCE_FILE)

    check_sample_freq(sample_freq)
    for sample_file in sample_files:
        progress += 1
        file_name_sanitized = sample_file.decode(sys.getfilesystemencoding()).encode(
            "UTF8")  # bug oplossen die zorgde dat bestanden met rare tekens niet in de database gevonden konden worden.
        print("\rGenerating tests with noise (%d/%d)..." % (progress, total_files), end="")
        sample_file_path = os.path.join(AUDIO_DIR, sample_file)
        song_id = dbhelper.get_song_id(file_name_sanitized)

        sample_freq, input = read(sample_file_path)
        check_sample_freq(sample_freq)

        # Bestanden aanmaken met ruis met SNR -3, 0, 3 en 6 dB
        for ratio in range(-3, 7, 3):
            audio_noise = add_noise(input, noise, 10, ratio)
            output_file = os.path.join(NOISE_DESTINATION_FOLDER, ("%d %d.wav" % (song_id, ratio)))
            write(output_file, SAMPLE_FREQ, audio_noise)


def run_tests_with_noise(test_folder):
    """
    Test alle gegenereerde bestanden met ruis uit de opgegeven map
    :param test_folder: map met gegenereerde bestanden met ruis
    """
    print("Preparing tests")
    test_files = file.find_all_files(test_folder)
    total_files = len(test_files)
    progress = 0
    results = []  # [ (song_id, snr, result, correct, confidence)
    for test_file in test_files:
        progress += 1
        print("\rRunning tests (%d/%d)..." % (progress, total_files), end="")
        test_file_path = os.path.join(test_folder, test_file)
        is_valid, song_id, snr = file.get_test_data_from_filename(test_file)
        if not is_valid:
            print("File %s does not have a filename that this program could understand, skipping...") % test_file
            continue
        success, confidences, found_song_id, result, time, title, artist = match.match_file(test_file_path)
        correct = (found_song_id == song_id)
        results.append([song_id, snr, found_song_id, correct, confidences[0][1]])
        print("(%s) %d with SNR %d found match %d with confidence %f" % (
            correct, song_id, snr, found_song_id, confidences[0][1]))

    total_tests = 0
    total_correct_3db = 0
    total_correct_minus3db = 0
    total_correct_6db = 0
    total_correct_minus6db = 0
    total_correct_0db = 0
    for result in results:
        total_tests += 1
        snr = result[1]
        if result[3]:
            if snr == -6:
                total_correct_minus6db += 1
            elif snr == -3:
                total_correct_minus3db += 1
            elif snr == 0:
                total_correct_0db += 1
            elif snr == 3:
                total_correct_3db += 1
            elif snr == 6:
                total_correct_6db += 1
    print("========================================================================")
    print(" Tests run: %d" % total_tests)
    print(" Tests per snr: %d" % (total_tests / 4))
    print(" Tests correct -3 db: %d" % total_correct_minus3db)
    print(" Tests correct 0 db: %d" % total_correct_0db)
    print(" Tests correct 3 db: %d" % total_correct_3db)
    print(" Tests correct 6 db: %d" % total_correct_6db)
    print("========================================================================")


def check_sample_freq(sample_freq):
    """
    Controleer of de bemonsteringsfrequentie gelijk is aan die van fragmenten toegevoegd aan de database
    :param sample_freq: de bemonsteringsfrequentie om te controleren
    """
    if sample_freq != SAMPLE_FREQ:
        print(
            "########################################################################################################")
        print(
            "Warning! Sample frequency is not the same as the config value. There probably won't be a reliable match!")
        print(
            "########################################################################################################")
