# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python2.6/site-packages/lbn/zenoss/base.py
# Compiled at: 2012-01-15 03:35:40
from AccessControl.class_init import InitializeClass
from AccessControl.Permissions import manage_properties
from OFS.SimpleItem import SimpleItem
from OFS.Folder import Folder
from OFS.PropertyManager import PropertyManager
from Products.ZenModel.ZenModelBase import ZenModelBase
from Products.ZenRelations.ZenPropertyManager import ZenPropertyManager

class PortalContent(ZenPropertyManager, ZenModelBase, SimpleItem):
    """
    the simplist type of content that supports FTI in Zenoss
    """
    __ac_permissions__ = ZenPropertyManager.__ac_permissions__ + ((manage_properties, ('getMenuIds', )),) + ZenModelBase.__ac_permissions__ + SimpleItem.__ac_permissions__
    manage_options = ZenPropertyManager.manage_options + SimpleItem.manage_options

    def zenPropertyIds(self, *args, **kw):
        """
        """
        return PropertyManager.propertyIds(self)

    def getZenRootNode(self):
        """Return the root node for our zProperties."""
        return self.getDmdRoot(self.dmdRootName)

    def getMenuIds(self):
        """
        our helper to supply menus for edit form

        the standard is to create menu's with the ZenPack name ...
        """
        return ()

    def breadCrumbs(self):
        """
        seems crumbs get dropped off ...
        """
        crumbs = ZenModelBase.breadCrumbs(self)
        if crumbs[(-1)][1] != self.getId():
            crumbs.append((self.absolute_url(1), self.getId()))
        return crumbs


InitializeClass(PortalContent)

class PortalFolder(Folder, PortalContent):
    """
    A container type
    """
    __ac_permissions__ = Folder.__ac_permissions__ + PortalContent.__ac_permissions__


InitializeClass(PortalFolder)