# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/esdrt/content/upgrades/38_39.py
# Compiled at: 2019-05-21 05:08:43
from zope.globalrequest import getRequest
from Products.CMFCore.utils import getToolByName
PROFILE_ID = 'profile-esdrt.content:default'

def upgrade(context, logger=None):
    if logger is None:
        from logging import getLogger
        logger = getLogger('esdrt.content.upgrades.38_39')
    reindex_index(context, logger)
    logger.info('Upgrade steps executed')
    return


def reindex_index(context, logger):
    setup = getToolByName(context, 'portal_setup')
    setup.runImportStepFromProfile(PROFILE_ID, 'catalog')
    logger.info('Reindexing indexes')
    catalog = getToolByName(context, 'portal_catalog')
    catalog.clearFindAndRebuild()