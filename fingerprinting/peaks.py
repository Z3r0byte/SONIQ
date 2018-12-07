def find_peaks(spectrum, xwindow, ywindow, min_amp=10):
    """
    Met deze functie worden pieken gezocht in de opgegeven data
    :param spectrum: de 2-D sprectrum Array
    :param xwindow: de hoeveelheid tijdblokken waarin rondom een punt gezocht wordt naar een hogere waarde
    :param ywindow: de hoeveelheid frequenties waarin rondom een punt gezocht wordt naar een hogere waarde
    :return:
    :rtype: 2-D array(freq, time) van pieken in :param spectrum
    """
    peaks = []
    freq_length = spectrum[0].size
    spectrum_length = (spectrum.size // spectrum[0].size)
    for spectrum_row in range(0, spectrum_length):
        freq_array = spectrum[spectrum_row]
        for freq_array_index in range(0, freq_length):  # selecteer een punt om te testen uit de geselecteerde rij
            if freq_array[freq_array_index] < min_amp:
                continue
            for spectrum_row2 in range(-ywindow, ywindow + 1):
                index_sum = spectrum_row + spectrum_row2
                if index_sum < 0 or index_sum >= spectrum_length:  # check of de index geldig is, zoniet, door naar de volgende iteratie
                    continue

                freq_array2 = spectrum[index_sum]
                for freq_array_index2 in range(-xwindow, xwindow + 1):
                    index_sum = freq_array_index + freq_array_index2  # check of de index geldig is, zoniet, door naar de volgende iteratie
                    if index_sum < 0 or index_sum >= freq_length:
                        continue
                    # Als het geselecteerde punt groter is dan het punt dat getest wordt is het geteste punt geen piek en stopt de loop
                    if freq_array2[index_sum] > freq_array[freq_array_index]:
                        break
                else:
                    continue
                break
            else:  # Als de bovenstaande loop zichzelf niet afsluit, is er geen grotere waarde gevonden en is het onderzochte punt dus een piek
                peaks.append([spectrum_row, freq_array_index])
    return peaks
