# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/adi/workingcopyflag/setuphandlers.py
# Compiled at: 2012-11-19 05:25:18
from Products.CMFCore.utils import getToolByName
from plone.app.iterate.interfaces import IBaseline

def setFlagForObjectsWithWorkingcopy(p):
    """Check if an item has a working copy and if yes, set workingcopy-flag to true.
    """
    p_types = getToolByName(p, 'portal_types')
    catalog = getToolByName(p, 'portal_catalog')
    for p_type in p_types:
        items = catalog.searchResults(portal_type=p_type)
        for item in items:
            obj = item.getObject()
            o_id = obj.getId()
            o_title = obj.Title()
            if IBaseline.providedBy(obj) == True:
                flag = obj.getField('workingcopyflag')
                flag.set(obj, True)
                obj.reindexObject()
                print 'INFO adi.workingcopyflag: workingcopyflag WAS set for:', o_id


def setupVarious(context):
    portal = context.getSite()
    if context.readDataFile('adi.workingyopyflag.marker.txt') is None:
        return
    else:
        setFlagForObjectsWithWorkingcopy(portal)
        return