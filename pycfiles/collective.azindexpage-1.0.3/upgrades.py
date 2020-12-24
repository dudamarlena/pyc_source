# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/ubuntu/workspace/src/collective/awstats_hitcounter/upgrades.py
# Compiled at: 2015-10-13 13:57:55
DEFAULT_PROFILE = 'profile-collective.awstats_hitcounter:default'

def upgrade_1100_to_1200(context):
    print 'Upgrading to 0.1.5'
    context.runImportStepFromProfile(DEFAULT_PROFILE, 'portlets')
    context.runImportStepFromProfile(DEFAULT_PROFILE, 'cssregistry')
    context.runImportStepFromProfile(DEFAULT_PROFILE, 'portal_registry')