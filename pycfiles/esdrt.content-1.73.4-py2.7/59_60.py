# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/esdrt/content/upgrades/59_60.py
# Compiled at: 2019-05-28 11:27:35
from Products.CMFCore.utils import getToolByName
from esdrt.content.upgrades import portal_workflow as upw

def upgrade(context):
    catalog = getToolByName(context, 'portal_catalog')
    wft = getToolByName(context, 'portal_workflow')
    type_mapping = upw.get_workflow_type_mapping(wft)
    queries = [
     dict(portal_type='Observation', review_state=[
      'phase2-pending', 'phase1-pending'], reindex_self_only=True),
     dict(portal_type='Comment', review_state='initial', reindex_self_only=True),
     dict(portal_type='Question', reindex_self_only=True),
     dict(portal_type='Conclusion', review_state='draft', reindex_self_only=True)]
    upw.upgrade(wft, catalog, type_mapping, queries)