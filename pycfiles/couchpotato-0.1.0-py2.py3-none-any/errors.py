# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/couchish/errors.py
# Compiled at: 2009-02-08 14:57:42
__doc__ = '\nViews we can build:\n    * by type, one view should be ok\n    * x_by_y views, from config (optional)\n    * ref and ref reversed views, one pair per relationship\n'

class CouchishError(Exception):
    """
    Base class type for all couchish exception types.
    """


class NotFound(CouchishError):
    """
    Document not found.
    """


class TooMany(CouchishError):
    """
    Too may documents were found.
    """