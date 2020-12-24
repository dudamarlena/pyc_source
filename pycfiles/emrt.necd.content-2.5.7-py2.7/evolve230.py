# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/emrt/necd/content/upgrades/evolve230.py
# Compiled at: 2019-02-15 13:51:23
import plone.api as api
from Products.CMFCore.utils import getToolByName

def delete_voc(portal):
    atvm = getToolByName(portal, 'portal_vocabularies')
    atvm._delObject('parameter')


def reindex_objs(portal):
    catalog = getToolByName(portal, 'portal_catalog')
    brains = catalog(portal_type='Observation')
    for brain in brains:
        brain.getObject().reindexObject(idxs=[
         'NFR_Code_Inventory', 'reference_year'])


def run(_):
    portal = api.portal.get()
    delete_voc(portal)
    reindex_objs(portal)