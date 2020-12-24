# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/aw/managersmanager/interfaces.py
# Compiled at: 2009-10-11 11:38:49
"""Public interfaces"""
from zope.interface import Interface

class IManagersManager(Interface):
    """What must be provided by managers manager
    """
    __module__ = __name__

    def listPlonePaths():
        """Must provide la list of Zope absolute paths of all Plone sites of
        this instance/cluster
        """
        pass

    def delManager(userid):
        """Removes an user from all Plone sites
        """
        pass

    def addManager(userid, password):
        """Adds a manager to all Plone sites
        """
        pass