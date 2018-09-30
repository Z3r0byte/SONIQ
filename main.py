import matplotlib.pyplot as plt
from scipy.io import wavfile
import numpy as np


# Fourier Transform
sample_freq, signal = wavfile.read('Audio Samples/01_This_Is_War_(Main_Theme).wav')
signal = signal.T[0]
intensity, freqs, time, im = plt.specgram(signal, NFFT=1024, Fs=sample_freq, noverlap=64)

# Getting right values for one time interval
freq_index = 13

presence = []
print intensity.size
row = intensity[freq_index]
for timefreq in row:
    presence.append(10 * np.log10(timefreq))  # Apply logarithmic scale, because dB
# Plot graph with intensity-frequency
plt.clf()
plt.plot(time, presence)
plt.title("Intensiteit bij tijd voor " + str(freqs[freq_index]) + "Hz")
plt.axis([0, 170, 0, 100])
plt.show()