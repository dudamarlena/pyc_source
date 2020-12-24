# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/adi/init/setuphandlers.py
# Compiled at: 2012-12-02 04:04:48


def deletePloneFolders(p):
    """Delete the standard Plone stuff that we don't need
    """
    existing = p.objectIds()
    itemsToDelete = ['Members', 'news', 'events', 'front-page']
    for item in itemsToDelete:
        if item in existing:
            p.manage_delObjects(item)


def setupVarious(context):
    portal = context.getSite()
    if context.readDataFile('adi.init.marker.txt') is None:
        return
    else:
        deletePloneFolders(portal)
        return