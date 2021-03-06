# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/esdrt/theme/upgrades/1000_1001.py
# Compiled at: 2019-05-21 05:08:56
from Products.CMFCore.utils import getToolByName
PROFILE_ID = 'profile-esdrt.theme:default'

def upgrade(context, logger=None):
    if logger is None:
        from logging import getLogger
        logger = getLogger('esdrt.theme.upgrades.1000_1001')
    setup = getToolByName(context, 'portal_setup')
    setup.runImportStepFromProfile(PROFILE_ID, 'jsregistry')
    logger.info('Reload JS')
    logger.info('Upgrade steps executed')
    return