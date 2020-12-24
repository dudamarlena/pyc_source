# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/sanhehu/Documents/GitHub/pygitrepo-project/pygitrepo/util.py
# Compiled at: 2018-08-05 14:29:05
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