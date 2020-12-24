# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bika/health/upgrade/to3004.py
# Compiled at: 2014-12-12 07:13:54
from Acquisition import aq_inner
from Acquisition import aq_parent
from Products.CMFCore import permissions
from Products.CMFCore.utils import getToolByName

def upgrade(tool):
    portal = aq_parent(aq_inner(tool))
    bsc = getToolByName(portal, 'bika_setup_catalog')
    addIndexAndColumn(bsc, 'getGender', 'FieldIndex')
    bsc.clearFindAndRebuild()
    return True


def addIndexAndColumn(catalog, index, indextype):
    try:
        catalog.addIndex(index, indextype)
    except:
        pass

    try:
        catalog.addColumn(index)
    except:
        pass