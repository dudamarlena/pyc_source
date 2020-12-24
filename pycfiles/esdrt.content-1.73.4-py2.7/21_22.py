# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/esdrt/content/upgrades/21_22.py
# Compiled at: 2019-05-21 05:08:43
from Products.CMFCore.utils import getToolByName
from esdrt.content.setuphandlers import prepareVocabularies
PROFILE_ID = 'profile-esdrt.content:default'

def upgrade(context, logger=None):
    if logger is None:
        from logging import getLogger
        logger = getLogger('esdrt.content.upgrades.21_22')
    reimport_vocabularies(context, logger)
    install_workflow(context, logger)
    install_contenttypes(context, logger)
    logger.info('Upgrade steps executed')
    return


def reimport_vocabularies(context, logger):
    atvm = getToolByName(context, 'portal_vocabularies')
    del atvm['conclusion_reasons']
    del atvm['conclusion_phase2_reasons']
    del atvm['finish_observation_reasons']
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
    if 'esd-conclusion-phase2-workflow' in wtool.keys():
        wtool.manage_delObjects(['esd-conclusion-phase2-workflow'])
    setup.runImportStepFromProfile(PROFILE_ID, 'rolemap')
    setup.runImportStepFromProfile(PROFILE_ID, 'workflow')
    setup.runImportStepFromProfile(PROFILE_ID, 'sharing')
    logger.info('Reinstalled Workflows, Roles and Permissions ')
    wtool.updateRoleMappings()
    logger.info('Security settings updated')


def install_contenttypes(context, logger):
    setup = getToolByName(context, 'portal_setup')
    setup.runImportStepFromProfile(PROFILE_ID, 'rolemap')
    setup.runImportStepFromProfile(PROFILE_ID, 'workflow')
    setup.runImportStepFromProfile(PROFILE_ID, 'sharing')
    setup.runImportStepFromProfile(PROFILE_ID, 'typeinfo')
    setup.runImportStepFromProfile(PROFILE_ID, 'difftool')
    logger.info('Content types installed')