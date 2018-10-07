import os
import re


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
