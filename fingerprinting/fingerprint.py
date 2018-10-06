import hashlib
import time

def fingerprint(peaks, xwindow=10, ywindow=5):
    hashes = []
    index = generate_index(peaks)
    index_len = len(index)
    peaks_len = len(peaks)
    i=0
    for peak in peaks:
        peaky = peak[0]
        peakx = peak[1]
        ywindow_low = peaky - ywindow
        ywindow_high = peaky + ywindow
        xwindow_low = peakx
        xwindow_high = peakx + xwindow
        for peak_test_row in range(-ywindow, ywindow + 1):
            peak_test_row_index = peaky + peak_test_row
            if peak_test_row_index >= index_len:
                break
            if peak_test_row_index < 0:
                continue

            start_search = index[peak_test_row_index]
            if peak_test_row_index < (len(index) - 1):
                stop_search = index[peak_test_row_index + 1]
            else:
                stop_search = peaks_len
            for peak_test_index in range(start_search, stop_search):
                i += 1
                peak_test = peaks[peak_test_index]
                if peak_test[0] != peak_test_row_index:
                    break
                if peak_test == peak:
                    continue

                if (ywindow_low <= peak_test[0] <= ywindow_high) and (
                        xwindow_low <= peak_test[1] <= xwindow_high):
                    hash = hashlib.sha256(str(peaky) + "-" + str(peak_test[0]) + "-" + str(peak_test[1] - peakx)).hexdigest()
                    hashes.append(hash)
                elif peak_test[1] <= xwindow_high:
                    continue
                else:
                    break
    print i
    return hashes


def generate_index(peaks):
    index = []
    index_index = 0
    peak_index = 0
    prev_peak_index = 0
    while index_index <= peaks[len(peaks) - 1][0]:
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
