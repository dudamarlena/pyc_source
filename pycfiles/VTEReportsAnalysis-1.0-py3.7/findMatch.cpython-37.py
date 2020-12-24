# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\VTEReportsAnalysis\findMatch.py
# Compiled at: 2020-05-05 05:09:04
# Size of source mod 2**32: 784 bytes
from collections import defaultdict

def shift_table(pattern):
    table = defaultdict(lambda : len(pattern))
    for index in range(0, len(pattern) - 1):
        table[pattern[index]] = len(pattern) - 1 - index

    return table


def horspool_match(pattern, text):
    table = shift_table(pattern)
    index = len(pattern) - 1
    while index <= len(text) - 1:
        match_count = 0
        while match_count < len(pattern) and pattern[(len(pattern) - 1 - match_count)] == text[(index - match_count)]:
            match_count += 1

        if match_count == len(pattern):
            return index - match_count + 1
        index += table[text[index]]

    return -1