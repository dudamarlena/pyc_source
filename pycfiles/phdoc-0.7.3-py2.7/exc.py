# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/phdoc/exc.py
# Compiled at: 2013-09-24 11:14:27


class MarkdocError(Exception):
    """An error occurred whilst running the phdoc utility."""
    pass


class AbortError(MarkdocError):
    """An exception occurred which should cause Markdoc to abort."""
    pass