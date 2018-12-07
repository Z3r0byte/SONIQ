import hashlib


def fingerprint(peaks, timewindow):
    """
    :returns een array van arrays met twee waarden (vingerafdrukken). De eerste waarde is een gedeelte van de SHA512 hash en de tweede waarde is het tijdstip van de hash
    :param peaks: de 2D array met pieken
    :param xwindow: Hoever vooruit gekeken moet worden om twee pieken te matchen tot een vingerafdruk
    :return:
    """
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
