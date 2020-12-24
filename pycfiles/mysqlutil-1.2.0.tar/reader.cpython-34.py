# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/halfak/env/3.4/lib/python3.4/site-packages/mysqltsv/reader.py
# Compiled at: 2016-01-30 13:35:32
# Size of source mod 2**32: 2490 bytes
__doc__ = '\nThis module provides a set of utilities for reading TSV files.\n\n.. autoclass:: mysqltsv.reader.Reader\n    :members:\n\n.. autofunction:: mysqltsv.functions.read\n\n'
import logging
from .errors import RowReadingError
from .row_type import RowGenerator
from .util import read_row
logger = logging.getLogger(__name__)

def raise_exception(lineno, line, e):
    raise RowReadingError(lineno, line, e)


class Reader:
    """Reader"""

    def __init__(self, f, headers=True, types=None, none_string='NULL', error_handler=raise_exception):
        self.f = f
        if headers == True:
            headers = list(read_row(f.readline()))
        else:
            if hasattr(headers, '__iter__'):
                headers = list(headers)
            else:
                headers = None
        self.row_type = RowGenerator(headers, types=types, none_string=none_string)
        self.headers = headers
        self.none_string = none_string
        self.error_handler = error_handler

    def __iter__(self):
        for i, line in enumerate(self.f):
            try:
                yield self.row_type(line)
            except Exception as e:
                lineno = i + 1 if self.headers is None else i + 2
                self.error_handler(lineno, line, e)

    def __next__(self):
        line = self.f.readline()
        if line != '':
            return self.row_type(line)
        raise StopIteration()