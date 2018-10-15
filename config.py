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
FINGERPRINT_TIME_WINDOW = 20
# Database
HOST = "localhost"
DATABASE = "SONIQ"
USER = "root"
PASSWORD = "password"