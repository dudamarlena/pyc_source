# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sanhehu/Documents/GitHub/pygitrepo-project/pygitrepo/util.py
# Compiled at: 2018-09-12 23:19:03
# Size of source mod 2**32: 348 bytes


def read(path, encoding='utf-8'):
    """Read string from text file.
    """
    with open(path, 'rb') as (f):
        return f.read().decode(encoding)


def write(s, path, encoding='utf-8'):
    """Write string to text file.
    """
    with open(path, 'wb') as (f):
        f.write(s.encode(encoding))