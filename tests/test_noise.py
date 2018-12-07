# coding=utf-8
from __future__ import print_function
import numpy as np
import random
import os
import sys
import files.filehandler as file
import database.databasehelper as dbhelper
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


def check_sample_freq(sample_freq):
    if sample_freq != SAMPLE_FREQ:
        print(
            "########################################################################################################")
        print(
            "Warning! Sample frequency is not the same as the config value. There probably won't be a reliable match!")
        print(
            "########################################################################################################")
