import matplotlib.pyplot as plt
import numpy as np


def plotSpecgram(signal, NFFT, sample_freq, noverlap):
    plt.specgram(signal, NFFT=NFFT, Fs=sample_freq, noverlap=noverlap)
    plt.show()


def applyFourier(signal, NFFT, sample_freq, noverlap):
    intensity, freqs, time, im = plt.specgram(signal, NFFT=NFFT, Fs=sample_freq, noverlap=noverlap)
    plt.clf()  # clear plot, because we don't need it anyway
    return intensity, freqs, time


def plotIntensityOfFreqOverTime(intensity, time, freqs, freq_index):
    freq = freqs[freq_index]
    intensity = intensity[freq_index]
    plt.clf()
    plt.plot(time, intensity)
    plt.title("Intensiteit bij tijd voor " + str(freq) + "Hz")
    plt.show()
