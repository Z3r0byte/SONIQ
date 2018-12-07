import matplotlib.pyplot as plt


def plot_specgram(signal, NFFT, sample_freq, noverlap):
    """
    Functie die gebruikt kan worden voor het plotten van een spectrogram tijdens debuggen
    :param signal: de array met het signaal
    :param NFFT: blokgrootte waarop de transformatie wordt toegepast
    :param sample_freq: De bemonsteringsfrequentie
    :param noverlap: Hoeveel punten de blokken elkaar moeten overlappen
    """
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
    """
    Functie die gebruikt kan worden om een grafiek te plotten van de sterkte van een bepaalde frequentie uitgezet tegen de tijd
    :param intensity: De ruwe data van het spectrogram
    :param time: De tijden
    :param freqs: De frequenties
    :param freq_index:  De index van de frequentie in :param freqs die geplot moet worden
    """
    freq = freqs[freq_index]
    intensity = intensity[freq_index]
    plt.clf()
    plt.plot(time, intensity)
    plt.title("Intensiteit bij tijd voor " + str(freq) + "Hz")
    plt.show()
