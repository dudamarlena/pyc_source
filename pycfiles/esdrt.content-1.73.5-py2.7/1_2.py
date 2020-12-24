# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/esdrt/content/upgrades/1_2.py
# Compiled at: 2019-05-21 05:08:43
from Products.CMFCore.utils import getToolByName
PROFILE_ID = 'profile-esdrt.content:default'

def upgrade(context, logger=None):
    if logger is None:
        from logging import getLogger
        logger = getLogger('esdrt.content.upgrades.1_2')
    upgrade_diff_tool(context, logger)
    enable_atd_spellchecker(context, logger)
    install_comments(context, logger)
    css_and_js(context, logger)
    install_workflow(context, logger)
    logger.info('Upgrade steps executed')
    return


def upgrade_diff_tool(context, logger):
    setup = getToolByName(context, 'portal_setup')
    setup.runImportStepFromProfile(PROFILE_ID, 'difftool')
    logger.info('Upgraded Diff Tool')


def enable_atd_spellchecker(context, logger):
    tinymce = getToolByName(context, 'portal_tinymce')
    tinymce.libraries_spellchecker_choice = 'AtD'
    tinymce.libraries_atd_service_url = 'service.afterthedeadline.com'
    logger.info('Enable AtD spellcheking plugin')


def install_comments(context, logger):
    setup = getToolByName(context, 'portal_setup')
    setup.runImportStepFromProfile(PROFILE_ID, 'typeinfo')
    setup.runImportStepFromProfile(PROFILE_ID, 'rolemap')
    setup.runImportStepFromProfile(PROFILE_ID, 'difftool')
    logger.info('Comments installed')


def css_and_js(context, logger):
    setup = getToolByName(context, 'portal_setup')
    setup.runImportStepFromProfile(PROFILE_ID, 'cssregistry')
    setup.runImportStepFromProfile(PROFILE_ID, 'jsregistry')
    logger.info('Reload CSS and JS')


def install_workflow(context, logger):
    setup = getToolByName(context, 'portal_setup')
    setup.runImportStepFromProfile(PROFILE_ID, 'workflow')
    logger.info('Resinstalled  Workflows')