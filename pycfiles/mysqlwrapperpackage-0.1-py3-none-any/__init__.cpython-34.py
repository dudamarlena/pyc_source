# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/halfak/env/3.4/lib/python3.4/site-packages/mysqltsv/__init__.py
# Compiled at: 2016-01-30 13:37:44
# Size of source mod 2**32: 1651 bytes
__doc__ = '\nThis library provides functionality for reading and producing MySQL compatible\nTab-Seperated Value files.  The most salient features of this library are\nthe `Reader()` and `Writer()` that enable reading and writing TSV files.\nThere\'s also a set of convenience functions for doing the same without\nconstructing a class -- see `read()` and `write()`.\n\n\nReading and Writing\n===================\n\nUse `Reader()` or `read()` to read TSV files:\n\n  >>> import io\n  >>> my_file = io.StringIO("user_id\tuser_text\tedits\n" +\n  ...                       "10\tFoobar_Barman\t2344\n" +\n  ...                       "11\tBarfoo_Fooman\t20\n" +\n  ...                       "NULL\t127.0.0.1\t42\n")\n  >>> reader = mysqltsv.Reader(my_file, types=[int, str, int])\n  >>> for row in reader:\n  ...     print(repr(row.user_id), repr(row[\'user_text\']), repr(row[2]))\n  ...\n  10 \'Foobar_Barman\' 2344\n  11 \'Barfoo_Fooman\' 20\n  None \'127.0.0.1\' 42\n\nUse `Writer()` or `write()` to write TSV files:\n\n  >>> import sys\n  >>> import mysqltsv\n  >>>\n  >>> writer = mysqltsv.Writer(sys.stdout, headers=[\'user_id\', \'user_text\', \'edits\'])\n  user_id\tuser_text\tedits\n  >>> writer.write([10, \'Foobar_Barman\', 2344])\n  10\tFoobar_Barman\t2344\n  >>> writer.write({\'user_text\': \'Barfoo_Fooman\', \'user_id\': 11, \'edits\': 20})\n  11\tBarfoo_Fooman\t20\n  >>> writer.write([None, "127.0.0.1", 42])\n  NULL\t127.0.0.1\t42\n\n:Authors:\n    * Aaron Halfaker `http://halfaker.info`\n\n:License: MIT -- see https://github.com/halfak/mysqltsv\n'
from .functions import read, write
from .reader import Reader
from .util import encode, decode, read_row, write_row
from .writer import Writer
__version__ = '0.0.7'