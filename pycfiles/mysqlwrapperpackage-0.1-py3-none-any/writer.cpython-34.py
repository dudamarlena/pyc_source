# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/halfak/env/3.4/lib/python3.4/site-packages/mysqltsv/writer.py
# Compiled at: 2015-08-27 09:46:24
# Size of source mod 2**32: 1278 bytes
__doc__ = '\nThis module provides a set of utilities for writing TSV files.\n\n.. autoclass:: mysqltsv.writer.Writer\n    :members:\n\n.. autofunction:: mysqltsv.functions.write\n\n'
import logging
from .util import write_row
logger = logging.getLogger(__name__)

class Writer:
    """Writer"""

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