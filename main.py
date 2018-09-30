import matplotlib.pyplot as plt
from scipy.io import wavfile
import numpy as np


#Fourier Transform
sample_freq, signal = wavfile.read('Audio Samples/audiocheck.net_400Hz_-5dBFS_1500Hz_-17dBFS_1s.wav')
intensity, freqs, time, im = plt.specgram(signal, NFFT=1024, Fs=sample_freq, noverlap=64)

#Getting right values for one time interval
presence = []
print intensity.size
for row in intensity:
    presence.append(10* np.log10(row[:1])) #Apply logarithmic scale, because dB

#Plot graph with intensity-frequency
plt.plot(freqs, presence)
plt.axis([0, 2000, 0, 100]) #Only to 2000 Hz, because test signal only has 400Hz and 1500Hz frequency
plt.show()