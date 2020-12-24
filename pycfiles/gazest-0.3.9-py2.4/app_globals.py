# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/gazest/lib/app_globals.py
# Compiled at: 2007-09-26 14:43:59
"""The application's Globals object"""
from pylons import config

class Globals(object):
    """Globals acts as a container for objects available throughout the
    life of the application
    """
    __module__ = __name__

    def __init__(self):
        """One instance of Globals is created during application
        initialization and is available during requests via the 'g'
        variable
        """
        pass