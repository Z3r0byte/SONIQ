def find_peaks(spectrum, window):
    """

    :param spectrum: the 2-D spectrum array
    :param window:  search-window, bigger number means less peaks
    :return:
    :rtype: 2-D array of peaks in spectrum
    """
    peaks = []
    freq_length = spectrum[0].size
    spectrum_length = (spectrum.size // spectrum[0].size)
    for spectrum_row in range(0, spectrum_length):  # select row
        freq_array = spectrum[spectrum_row]
        for freq_array_index in range(0, freq_length):  # select point in row to test if peak
            if freq_array[freq_array_index] < 0.1:
                continue
            for spectrum_row2 in range(-window, window):  # select test-row to check for higher values
                index_sum = spectrum_row + spectrum_row2
                if index_sum < 0 or index_sum >= spectrum_length:  # check if index is out of bounds
                    continue

                freq_array2 = spectrum[index_sum]
                for freq_array_index2 in range(-window, window):  # select test-point from test-row to check for higher values
                    index_sum = freq_array_index + freq_array_index2  # check if index is out of bounds
                    if index_sum < 0 or index_sum >= freq_length:
                        continue
                    # check if selected point is bigger than the point being tested
                    if freq_array2[index_sum] > freq_array[freq_array_index]:
                        break
                else:
                    continue
                break
            else:  # if the loop above doesn't kill itself, eg no bigger value found, than add current test point to peaks
                peaks.append([spectrum_row, freq_array_index])
    return peaks