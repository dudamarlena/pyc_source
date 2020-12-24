# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bika/health/upgrade/to3001.py
# Compiled at: 2014-12-12 07:13:54
from Acquisition import aq_inner
from Acquisition import aq_parent
from Products.CMFCore import permissions
from Products.CMFCore.utils import getToolByName

def upgrade(tool):
    portal = aq_parent(aq_inner(tool))
    bc = getToolByName(portal, 'bika_catalog')
    addIndexAndColumn(bc, 'getClientTitle', 'FieldIndex')
    addIndexAndColumn(bc, 'getPatientID', 'FieldIndex')
    addIndexAndColumn(bc, 'getPatientUID', 'FieldIndex')
    addIndexAndColumn(bc, 'getPatientTitle', 'FieldIndex')
    addIndexAndColumn(bc, 'getDoctorID', 'FieldIndex')
    addIndexAndColumn(bc, 'getDoctorUID', 'FieldIndex')
    addIndexAndColumn(bc, 'getDoctorTitle', 'FieldIndex')
    addIndexAndColumn(bc, 'getClientPatientID', 'FieldIndex')
    bc.clearFindAndRebuild()
    pc = getToolByName(portal, 'portal_catalog')
    addIndexAndColumn(pc, 'getDoctorID', 'FieldIndex')
    addIndexAndColumn(pc, 'getDoctorUID', 'FieldIndex')
    pc.clearFindAndRebuild()
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