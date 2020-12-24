# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/ryan/Dropbox/LITLAB/CODE/prosodic/dicts/fi/syllabifier/finnish_weight.py
# Compiled at: 2012-12-06 15:11:04
from finnish_functions import *

def syll_weight(syll_split):
    if len(syll_split[Syllable.nucleus]) > 1:
        return Weight.CVV
    else:
        if len(syll_split[Syllable.coda]) > 0:
            return Weight.CVC
        return Weight.CV


def make_weights(syllables):
    weights = []
    for syll in syllables:
        weights += [syll_weight(syll)]

    return weights