# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/esdrt/content/upgrades/41_42.py
# Compiled at: 2019-05-21 05:08:43
from Products.CMFCore.utils import getToolByName
from esdrt.content.roles.localrolesubscriber import grant_local_roles
import transaction
PROFILE_ID = 'profile-esdrt.content:default'

def upgrade(context, logger=None):
    if logger is None:
        from logging import getLogger
        logger = getLogger('esdrt.content.upgrades.41_42')
    reassign_localroles(context, logger)
    logger.info('Upgrade steps executed')
    return


def reassign_localroles(context, logger):
    catalog = getToolByName(context, 'portal_catalog')
    count = 0
    brains = catalog.unrestrictedSearchResults(portal_type='Observation')
    length = len(brains)
    for brain in brains:
        count = count + 1
        observation = brain.getObject()
        grant_local_roles(observation)
        logger.info('%s/%s: Granted to %s' % (count, length, brain.getPath()))
        if count % 100 == 0:
            transaction.commit()

    logger.info('Local roles granted')