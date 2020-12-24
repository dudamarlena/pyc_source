# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/danjac/petprojects/tesla/tests/output/ProjectName/projectname/lib/app_globals.py
# Compiled at: 2007-09-06 07:54:15
"""Pylons application's Globals object"""
from pylons import config

class Globals(object):
    """Globals acts as a container for objects available throughout the life of
    the application.
    """

    def __init__(self):
        """One instance of Globals is created during application initialization
        and is available during requests via the 'g' variable.
        """
        import projectname.model as model
        model.connect()