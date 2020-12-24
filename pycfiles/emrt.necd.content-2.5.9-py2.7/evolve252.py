# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/emrt/necd/content/upgrades/evolve252.py
# Compiled at: 2020-04-29 14:26:24
import logging, plone.api as api
logger = logging.getLogger(__name__)

def run(_):
    catalog = api.portal.get_tool('portal_catalog')
    rfs = [ b.getObject() for b in catalog(portal_type='ReviewFolder') ]
    for rf in rfs:
        if rf.type == 'projection':
            for obs in rf.objectValues():
                logger.info('Migrating %s', obs.absolute_url(1))
                obs.reindexObject()

    logger.info('Done!')