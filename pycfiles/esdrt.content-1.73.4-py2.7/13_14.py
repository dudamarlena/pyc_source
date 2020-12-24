# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/esdrt/content/upgrades/13_14.py
# Compiled at: 2019-05-21 05:08:43
from Products.CMFCore.utils import getToolByName
from esdrt.content.setuphandlers import prepareVocabularies
PROFILE_ID = 'profile-esdrt.content:default'

def upgrade(context, logger=None):
    if logger is None:
        from logging import getLogger
        logger = getLogger('esdrt.content.upgrades.13_14')
    css_and_js(context, logger)
    reimport_vocabularies(context, logger)
    logger.info('Upgrade steps executed')
    return


def reimport_vocabularies(context, logger):
    atvm = getToolByName(context, 'portal_vocabularies')
    del atvm['highlight']
    psetup = getToolByName(context, 'portal_setup')
    profile = psetup._getImportContext(PROFILE_ID)
    prepareVocabularies(context, profile)


def css_and_js(context, logger):
    setup = getToolByName(context, 'portal_setup')
    setup.runImportStepFromProfile(PROFILE_ID, 'cssregistry')
    setup.runImportStepFromProfile(PROFILE_ID, 'jsregistry')
    logger.info('Reload CSS and JS')


def install_workflow(context, logger):
    setup = getToolByName(context, 'portal_setup')
    wtool = getToolByName(context, 'portal_workflow')
    wtool.manage_delObjects([
     'esd-question-review-workflow',
     'esd-review-workflow',
     'esd-answer-workflow',
     'esd-comment-workflow',
     'esd-file-workflow'])
    setup.runImportStepFromProfile(PROFILE_ID, 'rolemap')
    setup.runImportStepFromProfile(PROFILE_ID, 'workflow')
    setup.runImportStepFromProfile(PROFILE_ID, 'sharing')
    setup.runImportStepFromProfile(PROFILE_ID, 'typeinfo')
    logger.info('Reinstalled  Workflows')
    wtool.updateRoleMappings()
    logger.info('Security settings updated')