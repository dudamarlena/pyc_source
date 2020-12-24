# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/altered/py23compat.py
# Compiled at: 2019-03-08 09:23:16


def strio():
    """
    This was difficult to get right in doctests when porting to Python 3.
    """
    try:
        from StringIO import StringIO
    except ImportError:
        from io import StringIO

    return StringIO()