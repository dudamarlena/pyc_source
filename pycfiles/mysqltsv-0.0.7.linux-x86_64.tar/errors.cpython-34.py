# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/halfak/env/3.4/lib/python3.4/site-packages/mysqltsv/errors.py
# Compiled at: 2015-08-27 09:46:16
# Size of source mod 2**32: 648 bytes
"""
.. autoclass:: mysqltsv.errors.RowReadingError
    :members:
"""

class RowReadingError(RuntimeError):
    __doc__ = '\n    Thrown when an error occurs during TSV row reading.\n    '

    def __init__(self, lineno, line, e):
        super().__init__('An error occurred while processing line #{0}:\n\t{1}'.format(lineno, repr(line[:1000])))
        self.lineno = lineno
        self.line = line
        self.e = e