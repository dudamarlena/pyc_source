# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/aw/managersmanager/management.py
# Compiled at: 2009-10-11 11:50:18
"""Managers management utilities"""
from zope.interface import implements
from zope.app.container.interfaces import IContainer
from Products.Five.browser import BrowserView
from interfaces import IManagersManager

class ManagersManager(BrowserView):
    __module__ = __name__
    implements(IManagersManager)

    def listPlonePaths(self):
        """see IManagersManager
        """
        out = self._listPlonePaths()
        return (out, True, '')

    def _listPlonePaths(self):
        out = []
        plone_mt = 'Plone Site'
        for obj in getPloneSites(self.context):
            path = ('/').join(obj.getPhysicalPath())
            out.append(path)

        return out

    def delManager(self, userid):
        """see IManagersManager
        """
        success = True
        paths = self._listPlonePaths()
        for path in paths:
            plone = self.context.restrictedTraverse(path)
            plone_pas = plone.acl_users
            plone_pas.userFolderDelUsers([userid])

        return (
         success, '')

    def addManager(self, userid, password):
        """see IManagersManager
        """
        success = True
        paths = self._listPlonePaths()
        for path in paths:
            plone = self.context.restrictedTraverse(path)
            plone_pas = plone.acl_users
            plone_pas.userFolderAddUser(userid, password, ['Manager'], [])

        return (
         success, '')


def getPloneSites(folderish):
    """Plone sites that are in that folderish
    """
    sites = []
    for item in folderish.objectValues():
        if item.meta_type == 'Plone Site':
            sites.append(item)
        elif IContainer.providedBy(item):
            sites.extend(getPloneSites(item))

    return sites