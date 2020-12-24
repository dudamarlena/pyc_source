# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/doakey/Sync/Programming/reflowrst/reflowrst/is_citation.py
# Compiled at: 2018-01-26 15:31:48
# Size of source mod 2**32: 449 bytes


def alpha_in_word(word):
    for char in word:
        if char.isalpha():
            return True

    return False


def is_citation(lines, index):
    """this must be called after the footnote checker"""
    if not lines[index].lstrip().startswith('.. ['):
        return False
    else:
        words = lines[index].lstrip().split(' ')
        if not words[1].endswith(']'):
            return False
        if alpha_in_word(words[1]):
            return True
        return False