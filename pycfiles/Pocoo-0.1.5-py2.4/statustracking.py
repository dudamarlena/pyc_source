# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/pocoo/pkg/core/statustracking.py
# Compiled at: 2006-12-26 17:18:01
"""
    pocoo.pkg.core.statustracking
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    This module implements some functions and classes used
    for tracking post/thread read/unread status information.

    :copyright: 2006 by Armin Ronacher.
    :license: GNU GPL, see LICENSE for more details.
"""
import marshal, time

class StatusTracker(object):
    """
    Base class that is passes a binary status tracking information
    dump and is used to check or update tracking informations.
    """
    __module__ = __name__

    def __init__(self, data):
        pass