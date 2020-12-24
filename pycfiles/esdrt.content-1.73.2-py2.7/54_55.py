# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/esdrt/content/upgrades/54_55.py
# Compiled at: 2019-05-21 05:08:43
from zope.component import getUtility
from zope.component.hooks import getSite
from esdrt.content.utilities.interfaces import ISetupReviewFolderRoles

def upgrade(_):
    portal = getSite()
    getUtility(ISetupReviewFolderRoles)(portal['2018'])