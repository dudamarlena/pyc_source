# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/esdrt/content/upgrades/60_61.py
# Compiled at: 2019-05-30 13:03:32
import logging, plone.api as api
from Products.CMFCore.utils import getToolByName
from esdrt.content.upgrades import portal_workflow as upw
logger = logging.getLogger(__name__)
IDX = 'reply_comments_by_mse'

def delete_index(context):
    catalog = getToolByName(context, 'portal_catalog')
    catalog.delIndex(IDX)


def reindex_index(catalog):
    brains = catalog(portal_type='Observation')
    len_brains = len(brains)
    for idx, brain in enumerate(brains, start=1):
        try:
            obj = brain.getObject()
            logger.info('[%s/%s] Updating %s...', idx, len_brains, brain.getURL())
            catalog.catalog_object(obj, idxs=(IDX,), update_metadata=1)
        except:
            logger.warn('[%s/%s] Skipped %s...', idx, len_brains, brain.getURL())
            continue


def upgrade(context):
    catalog = getToolByName(context, 'portal_catalog')
    wft = getToolByName(context, 'portal_workflow')
    type_mapping = upw.get_workflow_type_mapping(wft)
    queries = [
     dict(portal_type='Question', review_state=[
      'phase1-recalled-msa', 'phase2-recalled-msa'], reindex_self_only=True)]
    upw.upgrade(wft, catalog, type_mapping, queries)
    reindex_index(catalog)