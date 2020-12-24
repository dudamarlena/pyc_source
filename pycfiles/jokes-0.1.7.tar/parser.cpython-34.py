# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /media/jks/Root/Dev/python/jokes/jokes/modules/parser.py
# Compiled at: 2015-10-26 15:57:32
# Size of source mod 2**32: 503 bytes
from modules import cmd

class stream:
    _stream__stream = []

    def push(self, uin):
        self._stream__stream.append(uin)
        return uin


def read_words(*words):
    for word in words:
        print(word)

    return words


def parse(uin):
    """ Parses input string uin and returns the return value """
    words = uin.split()
    try:
        return getattr(cmd, words[0])(*words[1:])
    except AttributeError:
        return read_words(*words)