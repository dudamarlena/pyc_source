# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/emrt/necd/content/upgrades/evolve2201.py
# Compiled at: 2019-02-15 13:51:23
import logging, plone.api as api
from emrt.necd.content.observation import set_title_to_observation
logger = logging.getLogger(__name__)

def _update_brain(brains, index, column_index, value):
    """ Update the brain directly, modifying only the target field
        This is much faster than update_metadata=True, as that rebuilds the
        entire brain, calling all indexed attributes.
    """
    old_value = brains.get(index)
    _new_value = list(old_value)
    _new_value[column_index] = value
    brains[index] = tuple(_new_value)


def gen_get_observations(tool):
    brains = tool(portal_type='Observation')
    len_brains = len(brains)
    logger.info('Found %s brains.', len_brains)
    for idx, brain in enumerate(brains, start=1):
        yield (
         brain, brain.getObject())
        logger.info('Updating %s/%s.', idx, len_brains)


def run(_):
    tool = api.portal.get_tool('portal_catalog')
    _catalog = tool._catalog
    _brains = _catalog.data
    _uids = _catalog.uids
    _columns = _catalog.names
    for brain, obs in gen_get_observations(tool):
        tool.reindexObject(obs, idxs=['Title'], update_metadata=False)
        _index = _uids.get(brain.getPath())
        _column_index = _columns.index('Title')
        _update_brain(_brains, _index, _column_index, obs.title)