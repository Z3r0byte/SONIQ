from __future__ import print_function
print("SONIQ is loading...")
from config import AUDIO_DIR
import files.filehandler as files
import tests.test as tests
import tests.test_noise as noise
import server.server as server
import sys
import getopt
print("Ready")
print()


def help():
    print("SONIQ - Ruisbestendige audio-herkenning")
    print("Gebruik: main.py [optie]")
    print("    -t test_map              Draai tests met fragmenten in de opgegeven map")
    print("    -n test_map              Draai tests met automatisch gegenereerde (optie -g) bestanden in de opgegeven map")
    print("    -f                       Indexeer alle .wav bestanden in AUDIO_DIR uit config.py")
    print("    -g                       Genereer n testbestanden uit AUDIO_DIR met ruis NOISE_SOURCE_FILE (SNR = -6, -3, 0, 3, 6 db)")
    print("    -s                       Server modus")
    exit()


if not len(sys.argv[1:]):
    help()

try:
    opts, args = getopt.getopt(sys.argv[1:], "t:n:g:fs")
except getopt.GetoptError as error:
    print(str(error))
    help()


# De opgegeven argumenten verwerken
for opt, arg in opts:
    if opt == "-t":
        tests.run_tests(arg)
    elif opt == "-n":
        noise.run_tests_with_noise(arg)
    elif opt == "-g":
        noise.create_with_noise(arg)
    elif opt == "-f":
        if len(arg) >= 1:
            AUDIO_DIR = arg
        files.fingerprint_all(AUDIO_DIR)
    elif opt == "-s":
        server.start()
    else:
        help()
