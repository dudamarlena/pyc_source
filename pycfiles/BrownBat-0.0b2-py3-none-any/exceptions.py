# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.4-x86_64/egg/brownant/exceptions.py
# Compiled at: 2014-10-08 05:43:52
from __future__ import absolute_import, unicode_literals

class BrownantException(Exception):
    """The base exception of the Brownant framework."""


class NotSupported(BrownantException):
    """The given URL or other identity is from a platform which not support.

    This exception means any url rules of the app which matched the URL could
    not be found.
    """