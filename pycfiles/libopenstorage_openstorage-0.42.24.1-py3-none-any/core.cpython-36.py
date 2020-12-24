# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-ed191__6/pip/pip/_vendor/pytoml/core.py
# Compiled at: 2020-01-10 16:25:21
# Size of source mod 2**32: 509 bytes


class TomlError(RuntimeError):

    def __init__(self, message, line, col, filename):
        RuntimeError.__init__(self, message, line, col, filename)
        self.message = message
        self.line = line
        self.col = col
        self.filename = filename

    def __str__(self):
        return '{}({}, {}): {}'.format(self.filename, self.line, self.col, self.message)

    def __repr__(self):
        return 'TomlError({!r}, {!r}, {!r}, {!r})'.format(self.message, self.line, self.col, self.filename)