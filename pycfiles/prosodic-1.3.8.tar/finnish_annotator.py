# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ryan/DH/prosodic/dicts/fi/finnish_annotator.py
# Compiled at: 2012-12-06 15:11:04
from finnish_functions import *
from finnish_syllables import initialize_presyllabified, make_syllables
from finnish_weight import make_weights
from finnish_sonority import make_sonorities
from finnish_stress import make_stresses
from copy import deepcopy
import os.path
PRESYLL = 0
INITIAL = 1
SUFFIX = 2
COMPOUND = 3
import sys
dirself = ''
for path in sys.path:
    if os.path.sep + 'fi' in path:
        dirself = path

user_files = [
 os.path.join(dirself, 'presyllabified.txt'), os.path.join(dirself, 'initial.txt'), os.path.join(dirself, 'suffix.txt'), os.path.join(dirself, 'compound.txt')]
config_file = os.path.join(dirself, 'config.txt')
initial_compounds = []
suffixes = []
compound_dict = {}

def initialize_list(l, filename):
    try:
        f = open(filename, 'r')
        entries = f.readlines()
        f.close()
        for i in range(len(entries) - 1):
            l += [entries[i][:-1].lower()]

        l += [entries[(-1)].lower()]
    except IOError:
        print 'Error: File not found.'


def initialize_dict(dict, entries, separator):
    for entry in entries:
        entry = entry.lower()
        hyphen_free = entry.replace(separator, '')
        words = entry.split(separator)
        dict[hyphen_free] = words


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


def initialize_config():
    try:
        f = open(config_file, 'r')
        entries = f.readlines()
        f.close()
        if len(entries) != len(user_files):
            return
        for i in range(len(user_files) - 1):
            entries[i] = entries[i][:-1]

        for i in range(len(user_files)):
            if os.path.isfile(entries[i]):
                user_files[i] = entries[i]

    except IOError:
        print 'Error: Config file not found.'

    initialize_presyllabified(user_files[PRESYLL])
    initialize_list(initial_compounds, user_files[INITIAL])
    initialize_list(suffixes, user_files[SUFFIX])
    initialize_dict_from_file(compound_dict, user_files[COMPOUND])


initialize_config()

class Annotation:

    def __init__(self, word):
        self.word = word
        self.syllables = make_syllables(word)
        self.split_sylls = [ split_syllable(syll) for syll in self.syllables ]
        self.weights = make_weights(self.split_sylls)
        self.sonorities = make_sonorities(self.split_sylls)
        self.stresses = make_stresses(self.weights)

    def join(self, annotation):
        self.word += annotation.word
        self.syllables += annotation.syllables
        self.weights += annotation.weights
        self.sonorities += annotation.sonorities
        if len(annotation.stresses[0]) > 0:
            total_stresses = []
            for i in range(len(self.stresses)):
                for j in range(len(annotation.stresses)):
                    total_stresses += [deepcopy(self.stresses[i])]
                    total_stresses[(-1)] += [Stress.secondary]
                    total_stresses[(-1)] += annotation.stresses[j][1:]

            self.stresses = total_stresses


def split_initial_compounds(words):
    for word in initial_compounds:
        if words[(-1)].lower().startswith(word):
            return split_initial_compounds(words[:-1] + [words[(-1)][:len(word)]] + [words[(-1)][len(word):]])

    return words


def split_suffix(words):
    for suffix in suffixes:
        if words[(-1)].lower().endswith(suffix):
            boundary = len(words[(-1)]) - len(suffix)
            return words[:-1] + [words[(-1)][:-len(suffix)]] + [words[(-1)][-len(suffix):]]

    return words


def split_preannotated_compounds(words):
    result = []
    for i in range(len(words)):
        if words[i].lower() in compound_dict:
            result += compound_dict[words[i].lower()]
        else:
            result += [words[i]]

    return result


ORTHOGRAPHIC_COMPOUND_MARKER = '-'

def make_annotation(word):
    words = [
     word]
    words = split_initial_compounds(words)
    words = words[:-1] + words[(-1)].split(ORTHOGRAPHIC_COMPOUND_MARKER)
    words = split_suffix(words)
    words = split_preannotated_compounds(words)
    annotations = [ Annotation(word) for word in words ]
    for i in range(1, len(annotations)):
        annotations[0].join(annotations[i])

    return annotations[0]


def print_annotation(word_annotation):
    print annotation_string(word_annotation)
    print pattern_string(word_annotation)
    print


def mark(word):
    print_annotation(make_annotation(word))


def annotation_string(word_annotation):
    result = ''
    for i in range(len(word_annotation.stresses)):
        result += SYLLABLE_SEPARATOR
        for j in range(len(word_annotation.syllables)):
            if word_annotation.stresses[i][j] == Stress.primary:
                result += '´'
            elif word_annotation.stresses[i][j] == Stress.secondary:
                result += '`'
            result += word_annotation.syllables[j] + SYLLABLE_SEPARATOR

        result += '\n'

    return result[:-1]


def syll_pattern(weights):
    result = ''
    for w in weights:
        result += Weight.dict[w]

    return result


def stress_pattern(stresses):
    result = ''
    for i in range(len(stresses)):
        for s in stresses[i]:
            result += Stress.dict[s]

        result += ', '

    return result[:-2]


def sonority_pattern(sonorities):
    result = ''
    for s in sonorities:
        result += s

    return result


def pattern_string(word_annotation):
    return 'Weight: ' + syll_pattern(word_annotation.weights) + '   Stress: ' + stress_pattern(word_annotation.stresses) + '   Sonority: ' + sonority_pattern(word_annotation.sonorities)