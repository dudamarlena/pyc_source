# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/sc/psc/policy/upgrades/to01.py
# Compiled at: 2012-07-17 18:10:20
from zope import component
import logging
from Products.CMFCore.utils import getToolByName
from Products.GenericSetup import interfaces as gsinterfaces
from Products.GenericSetup.upgrade import listUpgradeSteps
from Products.ZCatalog.ProgressHandler import ZLogHandler
from sc.psc.policy.config import PRODUCTS

def upgrade0to1(context):
    """ Upgrade to version 1.0
    """
    setup = getToolByName(context, 'portal_setup')
    portal = getToolByName(context, 'portal_url').getPortalObject()
    migration = getToolByName(context, 'portal_migration')
    catalog = getToolByName(context, 'portal_catalog')
    portal_properties = getToolByName(context, 'portal_properties')
    qi = getToolByName(context, 'portal_quickinstaller')
    packages = [
     'collective.psc.blobstorage',
     'Products.PloneSoftwareCenter']
    dependencies = [ (name, locked, hidden, profile) for name, locked, hidden, install, profile, runProfile in PRODUCTS if name in packages and install ]
    for name, locked, hidden, profile in dependencies:
        qi.installProduct(name, locked=locked, hidden=hidden, profile=profile)

    oId = 'packages'
    oTitle = 'Packages Catalog'
    deleteDefaultContent(portal)
    createCatalog(portal, oId, oTitle)
    defaultPage(portal, oId)


def createCatalog(portal, oId, oTitle):
    """ Creation of a Software Center object inside our portal"""
    portal.invokeFactory(type_name='PloneSoftwareCenter', id=oId, title=oTitle)
    oPSC = portal[oId]
    oPSC.setStorageStrategy('blobstorage')
    oPSC.reindexObject()


def deleteDefaultContent(portal):
    """ Delete default (placeholder) content created by Plone"""
    contentIds = [
     'news', 'front-page', 'Members', 'events']
    contentIds = [ id for id in contentIds if id in portal.objectIds() ]
    portal.manage_delObjects(contentIds)


def defaultPage(portal, objectId):
    """ Define or packages catalog as default page"""
    portal.manage_changeProperties(default_page=objectId)