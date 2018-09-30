import matplotlib.pyplot as plt
from scipy.io import wavfile
import time

sample_freq, signal = wavfile.read('Audio Samples/01_This_Is_War_(Main_Theme)-short.wav')

NFFT = 512
fig, (ax2) = plt.subplots(1)
Pxx, freqs, bins, im = ax2.specgram(signal, NFFT=NFFT, Fs=sample_freq, noverlap=256)
plt.show()


fig, (ax2) = plt.subplots(1)
sample_freq, signal = wavfile.read('Audio Samples/01_This_Is_War_(Main_Theme)-record.wav')
Pxx, freqs, bins, im = ax2.specgram(signal, NFFT=NFFT, Fs=sample_freq, noverlap=256)
plt.show()

