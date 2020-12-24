# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/luto/snotes20/osf.py/venv/lib/python3.4/site-packages/osf/classes.py
# Compiled at: 2015-08-23 11:29:24
# Size of source mod 2**32: 957 bytes
from .timeutils import milliseconds_to_hhmmss
from modgrammar import ParseError

class ParentlessNoteError(ParseError):

    def __init__(self, line=-1):
        self.line = line
        self.message = 'parentless note'

    def __str__(self):
        return self.message + ' at line ' + str(self.line)


class Header:

    def __init__(self):
        self.kv = {}
        self.v = []


class OSFLine:

    def __init__(self):
        self.time = None
        self.text = ''
        self.link = None
        self.tags = []
        self.notes = []
        self._line = -1

    def osf(self, depth=0):
        parts = []
        if depth:
            parts.append('-' * depth)
        if self.time is not None:
            parts.append(milliseconds_to_hhmmss(self.time))
        parts.append(self.text)
        if self.link:
            parts.append('<' + self.link + '>')
        parts.extend(['#' + tag for tag in self.tags])
        return ' '.join(parts)