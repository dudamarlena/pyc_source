# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/pocoo/pkg/core/statustracking.py
# Compiled at: 2006-12-26 17:18:01
__doc__ = '\n    pocoo.pkg.core.statustracking\n    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n\n    This module implements some functions and classes used\n    for tracking post/thread read/unread status information.\n\n    :copyright: 2006 by Armin Ronacher.\n    :license: GNU GPL, see LICENSE for more details.\n'
import marshal, time

class StatusTracker(object):
    """
    Base class that is passes a binary status tracking information
    dump and is used to check or update tracking informations.
    """
    __module__ = __name__

    def __init__(self, data):
        pass