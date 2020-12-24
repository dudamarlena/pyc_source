# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ryan/Dropbox/LITLAB/CODE/prosodic/dicts/fi/syllabifier/finnish_syllables.py
# Compiled at: 2012-12-06 15:11:04
from finnish_functions import *

def initialize_dict(dict, entries, separator):
    for entry in entries:
        hyphen_free = entry.replace(separator, '').lower()
        boundary_list = [1]
        i = 1
        while i < len(entry):
            if entry[i] == separator:
                boundary_list += [1]
                i += 1
            else:
                boundary_list += [0]
            i += 1

        dict[hyphen_free] = boundary_list + [1]


def initialize_dict_from_file(dict, filename):
    try:
        f = open(filename, 'r')
        entries = f.readlines()
        f.close()
        for i in range(len(entries) - 1):
            entries[i] = entries[i][:-1]

        separator = entries[0]
        entries = entries[1:]
        initialize_dict(dict, entries, separator)
    except IOError:
        print 'Error: File not found.'


pre_sep_dict = {}

def initialize_presyllabified(filename):
    initialize_dict_from_file(pre_sep_dict, filename)


vowel_seq_dict = {}
VOWEL_SEQUENCES = [
 'ai-oi', 'ai-ui', 'au-oi', 'eu-oi', 'ie-oi', 'ie-ui', 'oi-oi', 'oi-ui', 'uo-ui', 'yö-yi', 'a-ei', 'a-oi', 'e-ai', 'e-oi', 'e-äi', 'e-öi', 'i-ai', 'i-au',
 'i-oi', 'i-äi', 'i-öi', 'o-ai', 'u-ai', 'u-ei', 'u-oi', 'y-ei', 'y-äi', 'ä-yi', 'ä-öi', 'ai-a', 'ai-e', 'ai-o', 'ai-u', 'au-a', 'au-e', 'eu-a', 'ie-a', 'ie-o', 'ie-u', 'ie-y',
 'i-o-a', 'i-o-e', 'i-ö-e', 'i-ö-ä', 'iu-a', 'iu-e', 'iu-o', 'oi-a', 'oi-e', 'oi-o', 'oi-u', 'ou-e', 'ou-o', 'u-e-a', 'ui-e', 'uo-a', 'uo-u', 'y-e-ä', 'yö-e', 'äi-e']
initialize_dict(vowel_seq_dict, VOWEL_SEQUENCES, '-')

def locate_long(chars):
    for i in range(len(chars) - 1):
        if is_long(chars[i:i + 2]):
            return i

    return -1


def is_inseparable_vowels(chars):
    return is_diphthong(chars) or is_long(chars)


def consonantal_onset(chars):
    return is_cluster(chars) or is_consonant(chars)


def apply_3c(word, boundary_list):
    sequence = 'ien'
    seq_len = len(sequence)
    if len(word) > seq_len:
        if word[-seq_len:] == sequence and word[(-(seq_len + 1))] != 't':
            boundary_list[-3] = 1


t4_final_v = ['u', 'y']
t4_diphthongs = set(vv for vv in DIPHTHONGS if vv[(-1)] in t4_final_v)

def apply_t4(word, boundary_list):
    for i in range(3, len(word)):
        if boundary_list[i] == 1:
            if is_consonant(word[(i - 1)]) and word[i - 3:i - 1] in t4_diphthongs:
                boundary_list[i - 2] = 1

    return word


def separate_vowels(vowels, boundary_list, start):
    v_len = len(vowels)
    if v_len == 2 and not is_inseparable_vowels(vowels):
        boundary_list[start + 1] = 1
    elif v_len > 2:
        if vowels in vowel_seq_dict:
            boundary_list[(start + 1):(start + v_len + 1)] = vowel_seq_dict[vowels][1:]
        else:
            boundary = locate_long(vowels)
            if boundary != -1:
                if boundary == 0:
                    boundary = 2
                    separate_vowels(vowels[boundary:], boundary_list, start + boundary)
                else:
                    separate_vowels(vowels[:boundary], boundary_list, start)
                boundary_list[start + boundary] = 1
            else:
                for i in range(len(vowels) - 1):
                    if not is_inseparable_vowels(vowels[i:i + 2]):
                        boundary_list[start + (i + 1)] = 1


def make_syllables(word):
    entry = word.lower()
    boundary_list = [1]
    if entry in pre_sep_dict:
        boundary_list = pre_sep_dict[entry]
    else:
        for i in range(1, len(entry)):
            boundary_list += [0]

        boundary_list += [1]
    make_splits(entry + SYLLABLE_SEPARATOR, boundary_list)
    syllables = introduce_splits(word, boundary_list)
    return syllables


def introduce_splits(word, boundary_list):
    result = []
    start = 0
    end = 0
    while end < len(word):
        end += 1
        if boundary_list[end] == 1:
            if word[start] == "'":
                result += [word[start + 1:end]]
            else:
                result += [word[start:end]]
            start = end

    return result


onset_lengths = [ cluster_length for cluster_length in CLUSTER_LENGTHS ]
onset_lengths += [1]

def make_splits(word, boundary_list):
    v_seq_start = 0
    v_seq_end = 0
    for i in range(len(word)):
        if is_vowel(word[i]):
            v_seq_end += 1
            if v_seq_end - v_seq_start == 1:
                for onset_length in onset_lengths:
                    cluster_start = i - onset_length
                    if cluster_start >= 0 and consonantal_onset(word[cluster_start:i]):
                        no_syllable_break = True
                        for h_index in range(cluster_start, i):
                            if boundary_list[h_index] == 1:
                                no_syllable_break = False

                        if no_syllable_break:
                            boundary_list[cluster_start] = 1
                        break

        else:
            if v_seq_end - v_seq_start > 1:
                separate_vowels(word[v_seq_start:v_seq_end], boundary_list, v_seq_start)
            v_seq_start = v_seq_end = i + 1

    apply_3c(word[:-1], boundary_list)
    apply_t4(word, boundary_list)