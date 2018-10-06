import fingerprinting.fourier_transform as fourier
import fingerprinting.peaks as peaks
import fingerprinting.fingerprint as fingerprint
from scipy.io.wavfile import read
import numpy as np

sample_freq, signal = read("Audio Samples/01_This_Is_War_(Main_Theme).wav")
signal = signal.T[0]

signalshort = signal[150000]
intensity, freqs, time = fourier.apply_fourier(signal, 1024, sample_freq, 256)
#fourier.plot_specgram(signal, 1024, sample_freq, 256)
#fourier.plot_intensity_of_freq_over_time(intensity, time, freqs, 162)

peaks_array = peaks.find_peaks(intensity, 5, 5)
hashes = fingerprint.fingerprint(peaks_array, 20, 10)

print len(peaks_array)
print len(hashes)
print "========================="

sample_freq2, signal2 = read("Audio Samples/01_This_Is_War_(Main_Theme)-record.wav")

signalshort2 = signal2[150000]
intensity2, freqs2, time2 = fourier.apply_fourier(signal2, 1024, sample_freq2, 256)

peaks_array2 = peaks.find_peaks(intensity2, 5, 5)
hashes2 = fingerprint.fingerprint(peaks_array2, 20, 10)
print len(peaks_array2)
print len(hashes2)
print "========================="

common = np.intersect1d(hashes, hashes2)
print "Amount of same hashes: " + str(len(common))
