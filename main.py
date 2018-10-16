# coding=utf-8
from config import AUDIO_DIR
import files.filehandler as files
import matching.match as match

files.fingerprint_all(AUDIO_DIR)

print "Matching song...."
match, confidence, song_id, result, time = match.match_file("Audio Samples/Opnames/Testopname-0059.wav")
if match:
    print result
else:
    print "Geen resultaat"
