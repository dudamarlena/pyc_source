# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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