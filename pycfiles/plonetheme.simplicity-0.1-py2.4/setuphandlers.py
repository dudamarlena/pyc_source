# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\plonetheme\simplicity\setuphandlers.py
# Compiled at: 2008-04-10 10:47:19
from zope.component import getUtility, getMultiAdapter
from plone.portlets.interfaces import IPortletManager
from plone.portlets.interfaces import IPortletAssignmentMapping

def setPortlets(portal):
    """Since there's not GenericSetup way to do this"""
    left_column = getUtility(IPortletManager, name='plone.leftcolumn')
    left_assignable = getMultiAdapter((portal, left_column), IPortletAssignmentMapping)
    right_column = getUtility(IPortletManager, name='plone.rightcolumn')
    right_assignable = getMultiAdapter((portal, right_column), IPortletAssignmentMapping)
    for name in left_assignable.keys():
        right_assignable[name] = left_assignable[name]
        del left_assignable[name]


def setupVarious(context):
    if context.readDataFile('plonetheme.simplicity_various.txt') is None:
        return
    portal = context.getSite()
    setPortlets(portal)
    return