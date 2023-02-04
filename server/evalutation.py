import math
from utils_fn import normalizeBetweenZeroToN


def get_discounted_gain(array, norm=True):
    discounted_gain = []
    for i, rel in enumerate(array):
        if i == 0:
            discounted_gain.append(rel)
        else:
            discounted_gain.append(rel / math.log2(i + 1))

    if norm:
        return [round(normalizeBetweenZeroToN(res, discounted_gain, 1), 4)
                for res in discounted_gain]

    return discounted_gain


def get_dcg(array):
    dcg = []
    for i, score in enumerate(array):
        if i == 0:
            dcg.append(score)
        else:
            dcg.append(dcg[i-1] + score)

    return [round(score,4) for score in dcg]
