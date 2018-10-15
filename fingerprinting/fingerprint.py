import hashlib


def fingerprint(peaks, timewindow):
    hashes = []
    peaks.sort(key=lambda x: x[1])
    for i in range(0, len(peaks) - 1):
        peak = peaks[i]
        for i2 in range(1, len(peaks) - (i+1)):
            if i + i2 >= len(peaks):
                break
            peak2 = peaks[i+i2]
            if peak2[1] <= (peak[1] + timewindow):
                hash = ["", 0]
                hash[0] = hashlib.sha512(str(peak[0]) + "-" + str(peak2[0]) + "-" + str(peak2[1] - peak[1])).hexdigest()[0:16]  # hex encoding, dus 16 tekens is 8 bytes
                hash[1] = peak[1]
                hashes.append(hash)
            else:
                break
    return hashes

# def fingerprint(peaks, xwindow=10, ywindow=5):
#     """
#     :returns een array van arrays met twee waarden. De eerste waarde is een SHA256 bits hash (de
#         vingerafdruk) en de tweede waarde is het tijdstip van de hash
#     :param peaks: de 2D array met pieken
#     :param xwindow: Hoever vooruit gekeken moet worden om twee pieken te matchen tot een vingerafdruk
#     :param ywindow: Hoeveel frequentiebanden er naar boven en naar benden gekeken moet worden om
#         een vingerafdruk te maken
#     :return:
#     """
#     hashes = []
#     index = generate_index(peaks)
#     index_len = len(index)
#     peaks_len = len(peaks)
#     for peak in peaks:
#         peaky = peak[0]
#         peakx = peak[1]
#         ywindow_low = peaky - ywindow
#         ywindow_high = peaky + ywindow
#         xwindow_low = peakx
#         xwindow_high = peakx + xwindow
#         for peak_test_row in range(ywindow_low, ywindow_high + 1):
#             if peak_test_row >= index_len:
#                 break
#             if peak_test_row < 0:
#                 continue
#
#             start_search = index[peak_test_row]
#             if peak_test_row < (len(index) - 1):
#                 stop_search = index[index_len - 1]
#                 for addition in range(0, index_len - peak_test_row - 1):
#                     if index[peak_test_row + addition] != index[peak_test_row]:
#                         stop_search = index[peak_test_row + addition]
#                         break
#             else:
#                 stop_search = peaks_len
#             for peak_test_index in range(start_search, stop_search):
#                 peak_test = peaks[peak_test_index]
#                 if peak_test[0] != peak_test_row:
#                     break
#                 if peak_test == peak:
#                     continue
#
#                 if (ywindow_low <= peak_test[0] <= ywindow_high) and (
#                         xwindow_low <= peak_test[1] <= xwindow_high):
#                     hash = ["", 0]
#                     hash[0] = hashlib.sha512(str(peaky) + "-" + str(peak_test[0]) + "-" + str(peak_test[1] - peakx)).hexdigest()[0:16]  # hex encoding, dus 16 tekens is 8 bytes
#                     hash[1] = peakx
#                     hashes.append(hash)
#                 elif peak_test[1] <= xwindow_high:
#                     continue
#                 else:
#                     break
#     return hashes
#
#
# def generate_index(peaks):
#     """
#     :returns een index met de index van de eerst voorkomende piek met een bepaalde frequentie, wanneer
#         er geen piek is met een frequentie wordt de index van de frequentie daarvoor gebruikt
#     :param peaks: 2D array van pieken
#     :return: 1D array van indexes
#     """
#     index = []
#     index_index = 0
#     peak_index = 0
#     prev_peak_index = 0
#     while index_index <= peaks[len(peaks) - 1][0]:
#         if peak_index == len(peaks):
#             break
#         if peaks[peak_index][0] == index_index:
#             index.append(peak_index)
#             prev_peak_index = peak_index
#             peak_index += 1
#             index_index += 1
#         else:
#             if peaks[peak_index][0] < index_index:
#                 peak_index += 1
#             else:
#                 index.append(prev_peak_index)
#                 index_index += 1
#     return index
