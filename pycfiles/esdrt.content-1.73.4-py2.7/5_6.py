# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/esdrt/content/upgrades/5_6.py
# Compiled at: 2019-05-21 05:08:43
from Products.CMFCore.utils import getToolByName
from esdrt.content.setuphandlers import prepareVocabularies
PROFILE_ID = 'profile-esdrt.content:default'

def upgrade(context, logger=None):
    if logger is None:
        from logging import getLogger
        logger = getLogger('esdrt.content.upgrades.5_6')
    reimport_vocabularies(context, logger)
    upgradeObservations(context, logger)
    install_workflow(context, logger)
    logger.info('Upgrade steps executed')
    return


def reimport_vocabularies(context, logger):
    atvm = getToolByName(context, 'portal_vocabularies')
    del atvm['eu_member_states']
    psetup = getToolByName(context, 'portal_setup')
    profile = psetup._getImportContext(PROFILE_ID)
    prepareVocabularies(context, profile)


def upgradeObservations(context, logger):
    """ check if any observation has old country assignments
    """
    COUNTRIES = {'au': 'at', 
       'cr': 'hr', 
       'et': 'ee', 
       'sv': 'sk'}
    brains = context.portal_catalog.unrestrictedSearchResults(portal_type='Observation', Country=COUNTRIES.keys())
    for brain in brains:
        observation = brain.getObject()
        old = observation.country
        new = COUNTRIES.get(old)
        observation.country = new
        logger.info('Country set for %s (%s -> %s)' % (observation.id, old, new))


def install_workflow(context, logger):
    setup = getToolByName(context, 'portal_setup')
    wtool = getToolByName(context, 'portal_workflow')
    wtool.manage_delObjects(['esd-question-review-workflow',
     'esd-review-workflow'])
    setup.runImportStepFromProfile(PROFILE_ID, 'workflow')
    logger.info('Reinstalled  Workflows')
    wtool.updateRoleMappings()
    logger.info('Security settings updated')