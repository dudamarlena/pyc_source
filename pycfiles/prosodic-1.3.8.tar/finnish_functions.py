# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ryan/Dropbox/LITLAB/CODE/prosodic/dicts/fi/syllabifier/finnish_functions.py
# Compiled at: 2012-12-06 15:11:04
SYLLABLE_SEPARATOR = '.'
CLUSTERS = set(['bl', 'br', 'dr', 'fl', 'fr', 'gl', 'gr', 'kl', 'kr', 'kv', 'pl', 'pr', 'cl', 'qv', 'schm'])
CLUSTER_LENGTHS = set(len(cluster) for cluster in CLUSTERS)
VOWELS = set(['i', 'e', 'ä', 'y', 'ö', 'a', 'u', 'o'])
DIPHTHONGS = set(['ai', 'ei', 'oi', 'äi', 'öi', 'au', 'eu', 'ou', 'ey', 'äy', 'öy', 'ui', 'yi', 'iu', 'iy', 'ie', 'uo', 'yö'])
CONSONANTS = set(['b', 'c', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'm', 'n', 'p', 'q', 'r', 's', 't', 'v', 'x', 'z', "'"])
SON_HIGH = set(['i', 'e', 'u', 'y'])
SON_LOW = set(['a', 'ä', 'o', 'ö'])

def is_vowel(ch):
    return ch in VOWELS


def is_consonant(ch):
    return ch in CONSONANTS


def is_cluster(ch):
    return ch in CLUSTERS


def is_diphthong(chars):
    return chars in DIPHTHONGS


def is_long(chars):
    return chars[0] == chars[1]


class Syllable:
    onset = 0
    nucleus = 1
    coda = 2


class Weight:
    CV = 0
    CVC = 1
    CVV = 2
    dict = {CV: 'L', CVC: 'H', CVV: 'H'}


def is_heavy(weight):
    return weight > Weight.CV


def is_heavier(weight1, weight2):
    return weight1 > weight2


class Stress:
    none = 0
    primary = 1
    secondary = 2
    dict = {none: 'U', primary: 'P', secondary: 'S'}


def split_syllable(syllable):
    result = []
    i = 0
    while i < len(syllable) and is_consonant(syllable[i].lower()):
        i += 1

    nucleus_start = i
    result += [syllable[0:nucleus_start]]
    while i < len(syllable) and is_vowel(syllable[i].lower()):
        i += 1

    coda_start = i
    result += [syllable[nucleus_start:coda_start]]
    result += [syllable[coda_start:]]
    return result