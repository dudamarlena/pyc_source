# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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