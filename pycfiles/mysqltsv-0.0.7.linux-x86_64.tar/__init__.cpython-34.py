# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/halfak/env/3.4/lib/python3.4/site-packages/mysqltsv/__init__.py
# Compiled at: 2016-01-30 13:37:44
# Size of source mod 2**32: 1651 bytes
"""
This library provides functionality for reading and producing MySQL compatible
Tab-Seperated Value files.  The most salient features of this library are
the `Reader()` and `Writer()` that enable reading and writing TSV files.
There's also a set of convenience functions for doing the same without
constructing a class -- see `read()` and `write()`.

Reading and Writing
===================

Use `Reader()` or `read()` to read TSV files:

  >>> import io
  >>> my_file = io.StringIO("user_id    user_text       edits
" +
  ...                       "10 Foobar_Barman   2344
" +
  ...                       "11 Barfoo_Fooman   20
" +
  ...                       "NULL       127.0.0.1       42
")
  >>> reader = mysqltsv.Reader(my_file, types=[int, str, int])
  >>> for row in reader:
  ...     print(repr(row.user_id), repr(row['user_text']), repr(row[2]))
  ...
  10 'Foobar_Barman' 2344
  11 'Barfoo_Fooman' 20
  None '127.0.0.1' 42

Use `Writer()` or `write()` to write TSV files:

  >>> import sys
  >>> import mysqltsv
  >>>
  >>> writer = mysqltsv.Writer(sys.stdout, headers=['user_id', 'user_text', 'edits'])
  user_id       user_text       edits
  >>> writer.write([10, 'Foobar_Barman', 2344])
  10    Foobar_Barman   2344
  >>> writer.write({'user_text': 'Barfoo_Fooman', 'user_id': 11, 'edits': 20})
  11    Barfoo_Fooman   20
  >>> writer.write([None, "127.0.0.1", 42])
  NULL  127.0.0.1       42

:Authors:
    * Aaron Halfaker `http://halfaker.info`

:License: MIT -- see https://github.com/halfak/mysqltsv
"""
from .functions import read, write
from .reader import Reader
from .util import encode, decode, read_row, write_row
from .writer import Writer
__version__ = '0.0.7'