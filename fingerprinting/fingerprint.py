def fingerprint(peaks, windowy=10, windowx=5):
    index = generate_index(peaks)


def generate_index(peaks):
    index = []
    index_index = 0
    peak_index = 0
    prev_peak_index = 0
    while index_index <= peaks[len(peaks)-1][0]:
        if peak_index == len(peaks):
            break
        if peaks[peak_index][0] == index_index:
            index.append(peak_index)
            prev_peak_index = peak_index
            peak_index += 1
            index_index += 1
        else:
            if peaks[peak_index][0] < index_index:
                peak_index += 1
            else:
                index.append(prev_peak_index)
                index_index += 1
    return index
