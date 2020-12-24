# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/heddex/tranquility/setuphandlers.py
# Compiled at: 2009-06-04 17:33:35
from zope.component import getUtility
from zope.component import getMultiAdapter
from plone.portlets.interfaces import IPortletAssignmentMapping
from plone.portlets.interfaces import ILocalPortletAssignmentManager
from plone.portlets.interfaces import IPortletManager
from heddex.tranquility.portlets import personaltools

def setupVarious(context):
    if context.readDataFile('heddex.tranquility_various.txt') is None:
        return
    portal = context.getSite()
    configurePortlets(portal)
    return


def configurePortlets(portal):
    leftColumn = getUtility(IPortletManager, name='plone.leftcolumn', context=portal)
    left = getMultiAdapter((portal, leftColumn), IPortletAssignmentMapping, context=portal)
    if 'personaltools' not in left:
        left['personaltools'] = personaltools.Assignment()