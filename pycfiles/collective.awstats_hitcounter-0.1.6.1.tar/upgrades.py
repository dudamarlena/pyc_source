# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ubuntu/workspace/src/collective/awstats_hitcounter/upgrades.py
# Compiled at: 2015-10-13 13:57:55
DEFAULT_PROFILE = 'profile-collective.awstats_hitcounter:default'

def upgrade_1100_to_1200(context):
    print 'Upgrading to 0.1.5'
    context.runImportStepFromProfile(DEFAULT_PROFILE, 'portlets')
    context.runImportStepFromProfile(DEFAULT_PROFILE, 'cssregistry')
    context.runImportStepFromProfile(DEFAULT_PROFILE, 'portal_registry')