# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/emrt/necd/content/upgrades/evolve2042.py
# Compiled at: 2019-02-15 13:51:23
from zope.component import getUtility
from zope.component.hooks import getSite
import plone.api as api
from emrt.necd.content.utilities.interfaces import ISetupReviewFolderRoles

def run(_):
    portal = getSite()
    target = portal.get('2018')
    if target:
        getUtility(ISetupReviewFolderRoles)(target)


def catalog(_):
    tool = api.portal.get_tool('portal_catalog')
    tool.manage_reindexIndex(ids=('GHG_Source_Category', ))