# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dj/workspace/dyson-py/lib/dyson/utils/quotes.py
# Compiled at: 2016-11-06 23:03:33
# Size of source mod 2**32: 313 bytes


def is_quoted(data):
    return len(data) > 1 and data[0] == data[(-1)] and data[0] in ('"', "'") and data[(-2)] != '\\'


def unquote(data):
    """ removes first and last quotes from a string, if the string starts and ends with the same quotes """
    if is_quoted(data):
        return data[1:-1]
    return data