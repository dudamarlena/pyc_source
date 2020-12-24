# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/halfak/env/3.4/lib/python3.4/site-packages/mysqltsv/writer.py
# Compiled at: 2015-08-27 09:46:24
# Size of source mod 2**32: 1278 bytes
"""
This module provides a set of utilities for writing TSV files.

.. autoclass:: mysqltsv.writer.Writer
    :members:

.. autofunction:: mysqltsv.functions.write

"""
import logging
from .util import write_row
logger = logging.getLogger(__name__)

class Writer:
    __doc__ = '\n    Constructs a new TSV row writer.\n\n    :Parameters:\n        f : `file`\n            A file pointer to write rows to\n        headers : `list`(`str`)\n            If a list of `str` is provided, use those strings as headers.\n            Otherwise, no headers are written.\n        none_string : `str`\n            A string that will be written as None when read.  (Defaults to\n            "NULL")\n    '

    def __init__(self, f, headers=None, none_string='NULL'):
        self.f = f
        self.none_string = none_string
        if headers != None:
            write_row(headers, self.f, none_string=self.none_string)
        self.headers = headers

    def write(self, row):
        """
        Writes a row to the output file.

        :Parameters:
            row : `list` | `dict` | :class:`~mysqltsv.row_type.AbstractRow`
                Datastructure representing the row to write
        """
        write_row(row, self.f, headers=self.headers, none_string=self.none_string)