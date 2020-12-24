# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ralph/bin/python/python35/lib/python3.5/site-packages/meltsubtitles/wordsRepoProc.py
# Compiled at: 2017-03-20 05:09:59
# Size of source mod 2**32: 432 bytes
import csv, sys
__author__ = 'celhipc'

def build_wordrepo(files):
    """
    build a set of the words which are known
    :param file:
    :return wordsrepo: a set
    """
    wordsRepo = set()
    for file in files:
        with open(file, 'r') as (finput):
            reader = csv.reader(finput)
            for words in reader:
                wordsRepo |= set(words)

    return wordsRepo