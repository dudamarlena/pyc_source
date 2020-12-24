# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/soynlp/hangle/_distance.py
# Compiled at: 2019-05-03 05:13:56
# Size of source mod 2**32: 2490 bytes
from collections import Counter
import numpy as np
from ._hangle import decompose

def levenshtein(s1, s2, cost={}):
    if len(s1) < len(s2):
        return levenshtein(s2, s1)
    if len(s2) == 0:
        return len(s1)

    def get_cost(c1, c2, cost):
        if c1 == c2:
            return 0
        return cost.get((c1, c2), 1)

    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [
         i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[(j + 1)] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + get_cost(c1, c2, cost)
            current_row.append(min(insertions, deletions, substitutions))

        previous_row = current_row

    return previous_row[(-1)]


def jamo_levenshtein(s1, s2):
    if len(s1) < len(s2):
        return jamo_levenshtein(s2, s1)
    if len(s2) == 0:
        return len(s1)

    def get_jamo_cost(c1, c2):
        if c1 == c2:
            return 0
        jamo1 = decompose(c1)
        jamo2 = decompose(c2)
        if jamo1 is None or jamo2 is None:
            return 1
        return levenshtein(decompose(c1), decompose(c2)) / 3

    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [
         i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[(j + 1)] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + get_jamo_cost(c1, c2)
            current_row.append(min(insertions, deletions, substitutions))

        previous_row = current_row

    return previous_row[(-1)]


def cosine_distance(s1, s2, unitfy=lambda x: Counter(x)):
    """distance = 1 - cosine similarity; [0, 2] """
    return s1 and s2 or 2
    d1 = unitfy(s1)
    d2 = unitfy(s2)
    prod = 0
    for c1, f in d1.items():
        prod += f * d2.get(c1, 0)

    return 1 - prod / np.sqrt(sum([f ** 2 for f in d1.values()]) * sum([f ** 2 for f in d2.values()]))


def jaccard_distance(s1, s2, unitfy=lambda x: set(x)):
    return s1 and s2 or 1
    s1_set = unitfy(s1)
    s2_set = unitfy(s2)
    return 1 - len(s1_set.intersection(s2_set)) / len(s1_set.union(s2_set))