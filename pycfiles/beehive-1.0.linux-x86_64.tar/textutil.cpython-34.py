# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python3.4/site-packages/beehive/textutil.py
# Compiled at: 2014-11-03 05:47:13
# Size of source mod 2**32: 1363 bytes
"""
Provides some utility functions related to text processing.
"""
from beehive.compat import unicode, basestring

def make_indentation(indent_size, part=' '):
    """
    Creates an indentation prefix string of the given size.
    """
    return indent_size * part


def indent(text, prefix):
    """
    Indent text or a number of text lines (with newline).

    :param lines:  Text lines to indent (as string or list of strings).
    :param prefix: Line prefix to use (as string).
    :return: Indented text (as unicode string).
    """
    lines = text
    newline = ''
    if isinstance(text, basestring):
        lines = text.splitlines(True)
    elif lines:
        if not lines[0].endswith('\n'):
            newline = '\n'
    if any([isinstance(line, unicode) for line in lines]):
        return newline.join([prefix + unicode(line) for line in lines])
    else:
        return newline.join([prefix + line.decode('utf-8') for line in lines])


def compute_words_maxsize(words):
    """
    Compute the maximum word size from a list of words (or strings).

    :param words: List of words (or strings) to use.
    :return: Maximum size of all words.
    """
    max_size = 0
    for word in words:
        if len(word) > max_size:
            max_size = len(word)
            continue

    return max_size