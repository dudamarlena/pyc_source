# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/twitabit/lib/app_globals.py
# Compiled at: 2008-01-19 12:54:35
"""The application's Globals object"""
from pylons import config

class Globals(object):
    """Globals acts as a container for objects available throughout the life of
    the application.
    """

    def __init__(self):
        """One instance of Globals is created during application initialization
        and is available during requests via the 'g' variable.
        """
        pass