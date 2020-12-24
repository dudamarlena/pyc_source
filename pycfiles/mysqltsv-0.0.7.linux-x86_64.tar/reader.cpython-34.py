# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/halfak/env/3.4/lib/python3.4/site-packages/mysqltsv/reader.py
# Compiled at: 2016-01-30 13:35:32
# Size of source mod 2**32: 2490 bytes
"""
This module provides a set of utilities for reading TSV files.

.. autoclass:: mysqltsv.reader.Reader
    :members:

.. autofunction:: mysqltsv.functions.read

"""
import logging
from .errors import RowReadingError
from .row_type import RowGenerator
from .util import read_row
logger = logging.getLogger(__name__)

def raise_exception(lineno, line, e):
    raise RowReadingError(lineno, line, e)


class Reader:
    __doc__ = '\n    Constructs a new TSV row reader -- which acts as an iterable of\n    :class:`~mysqltsv.row_type.AbstractRow`.\n\n    :Parameters:\n        f : `file`\n            A file pointer\n        headers : `bool` | `list`(`str`)\n            If True, read the first row of the file as a set of headers.  If a\n            list of `str` is provided, use those strings as headers.\n            Otherwise, assume no headers.\n        types : `list`( `callable` )\n            A list of `callable` to apply to the row values.  If none is\n            provided, all values will be read as `str`\n        none_string : `str`\n            A string that will be interpreted as None when read.  (Defaults to\n            "NULL")\n        error_handler : `callable`\n            A function that takes three arguements (lineno, line, exception)\n            that handles an error during row reading.  The default behavior is\n            to throw a :class:`mysqltsv.errors.RowReadingError`\n    '

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