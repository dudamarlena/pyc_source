# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/esdrt/content/upgrades/30_31.py
# Compiled at: 2019-05-21 05:08:43
from Products.CMFCore.utils import getToolByName
from esdrt.content.roles.localrolesubscriber import grant_local_roles
PROFILE_ID = 'profile-esdrt.content:default'

def upgrade(context, logger=None):
    if logger is None:
        from logging import getLogger
        logger = getLogger('esdrt.content.upgrades.30_31')
    install_sharing(context, logger)
    reassign_localroles(context, logger)
    logger.info('Upgrade steps executed')
    return


def install_sharing(context, logger):
    setup = getToolByName(context, 'portal_setup')
    setup.runImportStepFromProfile(PROFILE_ID, 'sharing')
    logger.info('Security settings updated')


def reassign_localroles(context, logger):
    catalog = getToolByName(context, 'portal_catalog')
    for brain in catalog.unrestrictedSearchResults(portal_type='Observation'):
        observation = brain.getObject()
        grant_local_roles(observation)
        logger.info('Granted to %s' % brain.getPath())

    logger.info('Local roles granted')