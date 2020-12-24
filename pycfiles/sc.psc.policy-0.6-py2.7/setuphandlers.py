# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/sc/psc/policy/setuphandlers.py
# Compiled at: 2012-07-17 18:10:20
from zope import component
import logging
from Products.CMFCore.utils import getToolByName
from Products.GenericSetup import interfaces as gsinterfaces
from Products.GenericSetup.upgrade import listUpgradeSteps
from Products.ZCatalog.ProgressHandler import ZLogHandler
try:
    from Products.CacheSetup import interfaces
    from Products.CacheSetup.enabler import enableCacheFu
    CACHEFU = True
except ImportError:
    CACHEFU = False

_PROJECT = 'sc.psc.policy'
_PROFILE_ID = 'sc.psc.policy:default'

def doUpgrades(context):
    """ If exists, run migrations
    """
    if context.readDataFile('sc.psc.policy.txt') is None:
        return
    else:
        logger = logging.getLogger(_PROJECT)
        site = context.getSite()
        setup_tool = getToolByName(site, 'portal_setup')
        cache = CACHEFU and getToolByName(context, 'portal_cache_settings', None)
        version = setup_tool.getLastVersionForProfile(_PROFILE_ID)
        upgradeSteps = listUpgradeSteps(setup_tool, _PROFILE_ID, version)
        sorted(upgradeSteps, key=lambda step: step['sortkey'])
        if cache:
            cache.setEnabled(False)
        for step in upgradeSteps:
            oStep = step.get('step')
            if oStep is not None:
                oStep.doStep(setup_tool)
                msg = 'Ran upgrade step %s for profile %s' % (oStep.title,
                 _PROFILE_ID)
                setup_tool.setLastVersionForProfile(_PROFILE_ID, oStep.dest)
                logger.info(msg)

        if cache:
            cache.setEnabled(True)
        return