# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/Products/slideshowfolder/Extensions/utils.py
# Compiled at: 2008-06-02 02:45:55
from Products.CMFCore.utils import getToolByName
from Products.slideshowfolder.browser import FolderSlideShowView

def restoreAllFolders(portal):
    """Walk the catalog and unmake all folders that appear to be slideshow folders"""
    count = 0
    catalog = getToolByName(portal, 'portal_catalog')
    for brain in catalog(portal_type='Folder'):
        folder = brain.getObject()
        view = FolderSlideShowView(folder, None)
        if view.isSlideshow():
            view.unmakeSlideshow()
            count += 1

    return 'Reverted %s slideshow folders to normal folders' % count


def removeAction(id_to_delete, portal_actions):
    """Delete a single action from portal actions"""
    actions = portal_actions._cloneActions()
    for action in actions:
        if action.id == id_to_delete:
            actions.remove(action)

    portal_actions._actions = tuple(actions)