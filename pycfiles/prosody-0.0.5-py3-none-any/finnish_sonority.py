# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/ryan/Dropbox/LITLAB/CODE/prosodic/dicts/fi/syllabifier/finnish_sonority.py
# Compiled at: 2012-12-06 15:11:04
from finnish_functions import *

def get_sonority(vowel):
    if len(vowel) == 0:
        return '?'
    return vowel[0].upper()


def make_sonorities(split_sylls):
    return [ get_sonority(syll[Syllable.nucleus]) for syll in split_sylls ]