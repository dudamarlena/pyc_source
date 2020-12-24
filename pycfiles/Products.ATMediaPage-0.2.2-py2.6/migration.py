# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/Products/ATMediaPage/migration.py
# Compiled at: 2010-06-03 12:43:08
import transaction
from zope.component import getUtility
from plone.browserlayer import utils as layerutils
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.interfaces.siteroot import IPloneSiteRoot
from Products.ATMediaPage.interfaces import IATMediaPageSpecific
from Products.ATMediaPage.exportimport import configureKupu, setVersionedTypes
import logging
logger = logging.getLogger('ATMediaPage-migration')
EXTENSION_PROFILES = ('Products.ATMediaPage:default', )

def emptyMigrate(self):
    """For dummy upgrade steps."""
    pass


def migrateTo02(context):
    """Replace deprecated layouts by new default view."""
    portal_types = getToolByName(context, 'portal_types')
    portal_setup = getToolByName(context, 'portal_setup')
    mp = getattr(portal_types, 'MediaPage', None)
    if mp:
        for extension_id in EXTENSION_PROFILES:
            portal_setup.runAllImportStepsFromProfile('profile-%s' % extension_id, purge_old=False)
            transaction.savepoint()

        view_methods = mp.view_methods
        query = {}
        query['portal_type'] = 'MediaPage'
        pages = context.portal_catalog.searchResults(query)
        for page in pages:
            obj = page.getObject()
            layout = obj.getLayout()
            if layout not in view_methods:
                obj.setLayout(mp.default_view)

    return


def migrateTo021(context):
    """Add new custom browserlayer."""
    if IATMediaPageSpecific not in layerutils.registered_layers():
        layerutils.register_layer(IATMediaPageSpecific, name='Products.ATMediaPage')
        logger.info('Browser layer "Products.ATMediaPage" installed.')
    site = getUtility(IPloneSiteRoot)
    kupu = getToolByName(site, 'kupu_library_tool', None)
    if kupu is not None:
        configureKupu(kupu)
        logger.info('Kupu configured for Products.ATMediaPage')
    return


def migrateTo1(context):
    """Add MediaPage to versioned types."""
    site = getUtility(IPloneSiteRoot)
    setVersionedTypes(site)
    logger.info('Versioned types configured for Products.ATMediaPage')