# CONFIG
# Flush the database if you change any of the values indicated with an [!] to prevent inaccurate results

# Algemeen
AUDIO_DIR = "Audio Samples/Test set"
# Spectrogram [!]
SAMPLE_FREQ = 44100
NFFT_WINDOW = 1024
N_OVERLAP = 512
# Pieken [!]
PEAK_TIME_WINDOW = 10
PEAK_FREQ_WINDOW = 10
# Vingerafdrukken [!]
FINGERPRINT_TIME_WINDOW = 10
# Matchen:
MIN_CONFIDENCE_FOR_STOP = 10
# Testen:
NOISE_SOURCE_FILE = "Audio Samples/Ruis.wav"
NOISE_DESTINATION_FOLDER = "Audio Samples/Gegenereerde tests"
# Database
HOST = "localhost"
DATABASE = "SONIQ"
USER = "root"
PASSWORD = "password"
# Server
SERVER_HOST = "0.0.0.0"
SERVER_PORT = 5000
