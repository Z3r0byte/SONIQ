import fingerprinting.fourier_transform as fourier
import fingerprinting.peaks as peaks
import fingerprinting.fingerprint as fingerprint
from scipy.io.wavfile import read
import matplotlib.pyplot as plt

sample_freq, signal = read("Audio Samples/01_This_Is_War_(Main_Theme)-short.wav")

signalshort = signal[150000]
intensity, freqs, time = fourier.apply_fourier(signal, 1024, sample_freq, 256)
#fourier.plot_specgram(signal, 1024, sample_freq, 256)
#fourier.plot_intensity_of_freq_over_time(intensity, time, freqs, 162)

peaks_array = peaks.find_peaks(intensity, 20)
fingerprint.fingerprint(peaks_array)

print peaks_array
x = []
y = []
for peak in peaks_array:
    x.append(peak[1]*time[0])
    y.append(peak[0]*freqs[1])
plt.scatter(x, y)
plt.axis([0, time.size*time[0], 0, freqs.size*freqs[1]])
plt.show()
