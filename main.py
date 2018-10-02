import fingerprinting.fourier_transform as fourier
from scipy.io.wavfile import read

sample_freq, signal = read("Audio Samples/01_This_Is_War_(Main_Theme)-short.wav")

signalshort = signal[:500000]
intensity, freqs, time = fourier.applyFourier(signal, 1024, sample_freq, 256)
fourier.plotIntensityOfFreqOverTime(intensity, time, freqs, 162)
