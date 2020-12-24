# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/esdrt/content/upgrades/44_45.py
# Compiled at: 2019-05-21 05:08:43
from zope.globalrequest import getRequest
from Products.CMFCore.utils import getToolByName
from esdrt.content.setuphandlers import prepareVocabularies
PROFILE_ID = 'profile-esdrt.content:default'

def upgrade(context, logger=None):
    if logger is None:
        from logging import getLogger
        logger = getLogger('esdrt.content.upgrades.44_45')
    install_workflow(context, logger)
    logger.info('Upgrade steps executed')
    return


def install_workflow(context, logger):
    setup = getToolByName(context, 'portal_setup')
    wtool = getToolByName(context, 'portal_workflow')
    setup.runImportStepFromProfile(PROFILE_ID, 'workflow')
    logger.info('Reinstalled Workflows')
    wtool.updateRoleMappings()
    logger.info('Security settings updated')