# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jphillips/go/src/github.com/lyft/toasted-marshmallow/toastedmarshmallow/utils.py
# Compiled at: 2019-06-13 15:03:45
# Size of source mod 2**32: 1172 bytes
import os
from contextlib import contextmanager

class IndentedString(object):
    __doc__ = 'Utility class for printing indented strings via a context manager.\n\n    '

    def __init__(self, content='', indent=4):
        self.result = []
        self._indent = indent
        self._IndentedString__indents = ['']
        if content:
            self.__iadd__(content)

    @contextmanager
    def indent(self):
        self._IndentedString__indents.append(self._IndentedString__indents[(-1)] + self._indent * ' ')
        try:
            yield
        finally:
            self._IndentedString__indents.pop()

    def __iadd__(self, other):
        if isinstance(other, IndentedString):
            for line in other.result:
                self.result.append(self._IndentedString__indents[(-1)] + line)

        else:
            self.result.append(self._IndentedString__indents[(-1)] + other)
        return self

    def __str__(self):
        return os.linesep.join(self.result)