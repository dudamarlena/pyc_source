# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/esdrt/content/upgrades/51_52.py
# Compiled at: 2019-05-21 05:08:43
from zope.globalrequest import getRequest
from Products.CMFCore.utils import getToolByName
import plone.api as api
PROFILE_ID = 'profile-esdrt.content:default'
STATES = ('phase2-closed', )
PERMISSION = 'Access contents information'

def upgrade(context, logger=None):
    if logger is None:
        from logging import getLogger
        logger = getLogger('esdrt.content.upgrades.51_52')
    update_permissions(context, logger)
    logger.info('Upgrade steps executed')
    return


def update_permissions(context, logger):
    wtool = getToolByName(context, 'portal_workflow')
    catalog = getToolByName(context, 'portal_catalog')
    brains = catalog(portal_type='Question', review_state=STATES)
    brains_len = len(brains)
    for idx, brain in enumerate(brains, start=1):
        content = brain.getObject()
        content.manage_permission(PERMISSION, acquire=1)
        content.reindexObjectSecurity()
        logger.info('Updated %s %s/%s.', brain.getURL(), idx, brains_len)