# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/halfak/env/3.4/lib/python3.4/site-packages/mysqltsv/errors.py
# Compiled at: 2015-08-27 09:46:16
# Size of source mod 2**32: 648 bytes
__doc__ = '\n.. autoclass:: mysqltsv.errors.RowReadingError\n    :members:\n'

class RowReadingError(RuntimeError):
    """RowReadingError"""

    def __init__(self, lineno, line, e):
        super().__init__('An error occurred while processing line #{0}:\n\t{1}'.format(lineno, repr(line[:1000])))
        self.lineno = lineno
        self.line = line
        self.e = e