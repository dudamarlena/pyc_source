# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/esdrt/content/roles/localrolesubscriber.py
# Compiled at: 2020-04-08 10:59:15
from Acquisition import aq_inner
from Acquisition import aq_parent
from plone import api
from esdrt.content.reviewfolder import IReviewFolder

def grant_local_roles(context):
    """ add local roles to the groups when adding an observation
    """
    country = context.country.lower()
    sector = context.ghg_source_category_value()
    applies_to = [context]
    parent = aq_parent(aq_inner(context))
    if IReviewFolder.providedBy(parent):
        applies_to.append(parent)
    context.__ac_local_roles_block__ = True
    for obj in applies_to:
        _roles_start = obj.get_local_roles()
        api.group.grant_roles(groupname='extranet-esd-ghginv-sr-%s-%s' % (sector, country), roles=[
         'ReviewerPhase1'], obj=obj)
        api.group.grant_roles(groupname='extranet-esd-ghginv-qualityexpert-%s' % sector, roles=[
         'QualityExpert'], obj=obj)
        api.group.grant_roles(groupname='extranet-esd-esdreview-reviewexp-%s-%s' % (
         sector, country), roles=[
         'ReviewerPhase2'], obj=obj)
        api.group.grant_roles(groupname='extranet-esd-esdreview-leadreview-%s' % country, roles=[
         'LeadReviewer'], obj=obj)
        api.group.grant_roles(groupname='extranet-esd-countries-msa-%s' % country, roles=[
         'MSAuthority'], obj=obj)
        _roles_end = obj.get_local_roles()
        if _roles_end != _roles_start:
            obj.reindexObjectSecurity()