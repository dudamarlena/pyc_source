# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/couchish/errors.py
# Compiled at: 2009-02-08 14:57:42
"""
Views we can build:
    * by type, one view should be ok
    * x_by_y views, from config (optional)
    * ref and ref reversed views, one pair per relationship
"""

class CouchishError(Exception):
    """
    Base class type for all couchish exception types.
    """
    pass


class NotFound(CouchishError):
    """
    Document not found.
    """
    pass


class TooMany(CouchishError):
    """
    Too may documents were found.
    """
    pass