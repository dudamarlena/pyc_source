# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/linseed/read.py
# Compiled at: 2011-05-31 11:44:21
from . import parsing

def _read(filename, parser=parsing.basic_parse):
    """Read a file and return the parsed results.

    Args:
      * filename: The name of the file to read.
      * parser: The parser to use (see ``parsing`` module.)

    Returns:
      The output of ``parser``.
    """
    with open(filename, 'r') as (f):
        return parser(list(f))