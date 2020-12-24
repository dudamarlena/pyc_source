# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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