import matplotlib.pyplot as plt


def plot_specgram(signal, NFFT, sample_freq, noverlap):
    plt.specgram(signal, NFFT=NFFT, Fs=sample_freq, noverlap=noverlap)
    plt.show()


def apply_fourier(signal, NFFT, sample_freq, noverlap):
    """
    Past de Fourier transformatie toe op het gegeven signaal
    :param signal: de array met het signaal
    :param NFFT: blokgrootte waarop de transformatie wordt toegepast
    :param sample_freq: De bemonsteringsfrequentie
    :param noverlap: Hoeveel punten de blokken elkaar moeten overlappen
    :return:
        intensity (2D-array): de uitkomsten van de fourier transformatie op een bepaald tijdstip voor een bepaalde frequentie
        freqs (1D-array): de frequenties waarop de transformaties toegepast zijn
        time (1D-array): de middelste tijd van elk blok
    """
    intensity, freqs, time, im = plt.specgram(signal, NFFT=NFFT, Fs=sample_freq, noverlap=noverlap)
    plt.clf()  # clear plot, because we don't need it anyway
    return intensity, freqs, time


def plot_intensity_of_freq_over_time(intensity, time, freqs, freq_index):
    freq = freqs[freq_index]
    intensity = intensity[freq_index]
    plt.clf()
    plt.plot(time, intensity)
    plt.title("Intensiteit bij tijd voor " + str(freq) + "Hz")
    plt.show()
