from __future__ import print_function
from config import AUDIO_DIR
import files.filehandler as files
import tests.test as tests
import sys
import getopt


def help():
    print("SONIQ - ruisbestendige audio herkenning")
    print("Gebruik: main.py [optie]")
    print("    -t test_map              Draai tests met fragmenten in de opgegeven map")
    print("    -f                       Indexeer alle .wav bestanden in AUDIO_DIR uit config.py")
    print("    -s                       Server modus")
    exit()


if not len(sys.argv[1:]):
    help()

try:
    opts, args = getopt.getopt(sys.argv[1:], "t:fs")
except getopt.GetoptError as error:
    print(str(error))
    help()

for opt, arg in opts:
    if opt == "-t":
        tests.run_tests(arg)
    elif opt == "-f":
        if len(arg) >= 1:
            AUDIO_DIR = arg
        files.fingerprint_all(AUDIO_DIR)
    elif opt == "-s":
        print("WIP")
    else:
        help()
