# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/socialcommerce/apps/mptt/exceptions.py
# Compiled at: 2009-10-31 23:19:40
"""
MPTT exceptions.
"""

class InvalidMove(Exception):
    """
    An invalid node move was attempted.

    For example, attempting to make a node a child of itself.
    """
    pass