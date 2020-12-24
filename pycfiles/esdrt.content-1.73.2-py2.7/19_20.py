# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/esdrt/content/upgrades/19_20.py
# Compiled at: 2019-05-21 05:08:43
from Products.CMFCore.utils import getToolByName
from plone import api
from esdrt.content.setuphandlers import prepareVocabularies
PROFILE_ID = 'profile-esdrt.content:default'

def upgrade(context, logger=None):
    if logger is None:
        from logging import getLogger
        logger = getLogger('esdrt.content.upgrades.19_20')
    reimport_vocabularies(context, logger)
    install_workflow(context, logger)
    logger.info('Upgrade steps executed')
    return


def reimport_vocabularies(context, logger):
    atvm = getToolByName(context, 'portal_vocabularies')
    del atvm['finish_observation_reasons']
    del atvm['eea_member_states']
    psetup = getToolByName(context, 'portal_setup')
    profile = psetup._getImportContext(PROFILE_ID)
    prepareVocabularies(context, profile)


def install_workflow(context, logger):
    setup = getToolByName(context, 'portal_setup')
    wtool = getToolByName(context, 'portal_workflow')
    wtool.manage_delObjects([
     'esd-answer-workflow',
     'esd-comment-workflow',
     'esd-conclusion-workflow',
     'esd-file-workflow',
     'esd-question-review-workflow',
     'esd-reviewtool-folder-workflow',
     'esd-review-workflow'])
    setup.runImportStepFromProfile(PROFILE_ID, 'rolemap')
    setup.runImportStepFromProfile(PROFILE_ID, 'workflow')
    setup.runImportStepFromProfile(PROFILE_ID, 'sharing')
    logger.info('Reinstalled Workflows, Roles and Permissions ')
    wtool.updateRoleMappings()
    logger.info('Security settings updated')