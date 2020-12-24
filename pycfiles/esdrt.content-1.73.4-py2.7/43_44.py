# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/esdrt/content/upgrades/43_44.py
# Compiled at: 2019-05-21 05:08:43
from Products.CMFCore.utils import getToolByName
import transaction
PROFILE_ID = 'profile-esdrt.content:default'

def upgrade(context, logger=None):
    if logger is None:
        from logging import getLogger
        logger = getLogger('esdrt.content.upgrades.43_44')
    update_catalog(context, logger)
    update_rolemap(context, logger)
    catalog_metadata(context, logger)
    logger.info('Upgrade steps executed')
    return


def update_rolemap(context, logger):
    setup = getToolByName(context, 'portal_setup')
    setup.runImportStepFromProfile(PROFILE_ID, 'rolemap')
    transaction.commit()


def update_catalog(context, logger):
    setup = getToolByName(context, 'portal_setup')
    setup.runImportStepFromProfile(PROFILE_ID, 'catalog')
    transaction.commit()


def catalog_metadata(context, logger):
    catalog = getToolByName(context, 'portal_catalog')
    logger.info('Reindexing')
    brains = catalog(portal_type='Observation')
    length = len(brains)
    count = 0
    for b in brains:
        count = count + 1
        obj = b.getObject()
        obj.edit()
        logger.info('%s/%s: %s reindexed' % (count, length, obj.getId()))
        if count % 100 == 0:
            transaction.commit()
            logger.info('transaction committed')