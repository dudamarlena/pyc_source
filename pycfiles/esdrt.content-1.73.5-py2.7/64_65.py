# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/esdrt/content/upgrades/64_65.py
# Compiled at: 2020-03-02 04:53:24
import logging
from Products.CMFCore.utils import getToolByName
import transaction
LOG = logging.getLogger(__name__)

def upgrade(context):
    catalog = getToolByName(context, 'portal_catalog')
    objects = [ b.getObject() for b in catalog(portal_type=['Observation']) ]
    len_objects = len(objects)
    for idx, obs in enumerate(objects, start=1):
        if idx % 100 == 0:
            transaction.savepoint(optimistic=True)
            LOG.info('Done: %s/%s', idx, len_objects)
        catalog.reindexObject(obs, update_metadata=True)