# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/emrt/necd/content/upgrades/evolve2045.py
# Compiled at: 2019-02-15 13:51:23
import logging, plone.api as api
from emrt.necd.content.observation import set_title_to_observation
logger = logging.getLogger(__name__)

def gen_get_observations(tool):
    brains = tool(portal_type='Observation')
    len_brains = len(brains)
    logger.info('Found %s brains.', len_brains)
    for idx, brain in enumerate(brains, start=1):
        yield brain.getObject()
        logger.info('Updating %s/%s.', idx, len_brains)


def run(_):
    tool = api.portal.get_tool('portal_catalog')
    for obs in gen_get_observations(tool):
        _current_roles = obs.get_local_roles()
        _principals = [ p for p, _ in _current_roles if 'sector' in p ]
        obs.manage_delLocalRoles(_principals)
        set_title_to_observation(obs, None)

    return