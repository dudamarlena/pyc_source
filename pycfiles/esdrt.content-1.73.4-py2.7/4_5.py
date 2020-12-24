# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/esdrt/content/upgrades/4_5.py
# Compiled at: 2019-05-21 05:08:43
from Products.CMFCore.utils import getToolByName
PROFILE_ID = 'profile-esdrt.content:default'

def upgrade(context, logger=None):
    if logger is None:
        from logging import getLogger
        logger = getLogger('esdrt.content.upgrades.4_5')
    install_workflow(context, logger)
    logger.info('Upgrade steps executed')
    return


def install_workflow(context, logger):
    setup = getToolByName(context, 'portal_setup')
    wtool = getToolByName(context, 'portal_workflow')
    wtool.manage_delObjects(['esd-question-review-workflow'])
    setup.runImportStepFromProfile(PROFILE_ID, 'workflow')
    logger.info('Reinstalled  Workflows')