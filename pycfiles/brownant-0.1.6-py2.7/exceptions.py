# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.4-x86_64/egg/brownant/exceptions.py
# Compiled at: 2014-10-08 05:43:52
from __future__ import absolute_import, unicode_literals

class BrownantException(Exception):
    """The base exception of the Brownant framework."""
    pass


class NotSupported(BrownantException):
    """The given URL or other identity is from a platform which not support.

    This exception means any url rules of the app which matched the URL could
    not be found.
    """
    pass