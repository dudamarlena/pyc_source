# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/esdrt/content/upgrades/48_49.py
# Compiled at: 2019-05-21 05:08:43
from logging import getLogger
from zope.component import getUtility
from zope.schema.interfaces import IVocabularyFactory
from Products.CMFCore.utils import getToolByName
import plone.api as api

def upgrade(context, logger=None):
    if logger is None:
        logger = getLogger('esdrt.content.upgrades.48_49')
    catalog = api.portal.get_tool('portal_catalog')
    brains = catalog(portal_type='Observation')
    brains_len = len(brains)
    logger.info('Found %s brains.', brains_len)
    observations = (brain.getObject() for brain in brains)
    for idx, observation in enumerate(observations, start=1):
        catalog.catalog_object(observation, idxs=('observation_status', ), update_metadata=1)
        if idx % 50 == 0:
            logger.info('Done %s/%s.', idx, brains_len)

    return