# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-universal/egg/c2/patch/atrefs/methods.py
# Compiled at: 2010-07-09 01:18:04
"""
methods.py

Created by Manabu Terada on 2010-07-08.
Copyright (c) 2010 CMScom. All rights reserved.
"""
from DateTime import DateTime
from AccessControl import Unauthorized
from AccessControl import getSecurityManager
from Products.CMFCore.utils import getToolByName
from Products.Archetypes import config
from Products.CMFCore.permissions import View
from Products.Archetypes.Referenceable import Referenceable
from Products.CMFPlone.CatalogTool import getObjPositionInParent
from logging import getLogger
logger = getLogger(__name__)
info = logger.info

def _check_view_permission(obj):
    return getSecurityManager().checkPermission(View, obj)


def _check_effective_range_permission(obj):
    now = DateTime()
    effectiveDate = obj.getEffectiveDate()
    expirationDate = obj.getExpirationDate()
    if effectiveDate and effectiveDate > now:
        return False
    else:
        if expirationDate and expirationDate < now:
            return False
        return True


def getSecureRefs(self, relationship=None, targetObject=None):
    """get all the referenced objects for this object"""
    tool = getToolByName(self, config.REFERENCE_CATALOG)
    refs = tool.getReferences(self, relationship, targetObject=targetObject)
    if refs:
        lst = []
        for ref in refs:
            obj = ref.getTargetObject()
            if _check_view_permission(obj) and _check_effective_range_permission(obj):
                lst.append(obj)

        return lst
    return []


def getSecureBRefs(self, relationship=None, targetObject=None):
    """get all the back referenced objects for this object"""
    tool = getToolByName(self, config.REFERENCE_CATALOG)
    refs = tool.getBackReferences(self, relationship, targetObject=targetObject)
    if refs:
        lst = []
        for ref in refs:
            obj = ref.getSourceObject()
            if _check_view_permission(obj) and _check_effective_range_permission(obj):
                lst.append(obj)

        return lst
    return []


def _get_sorted_lst(lst, sort_key, order):
    if sort_key is None:
        sort_key = 'Date'

    def _get_sorted_key(obj):
        try:
            o = getattr(obj, sort_key, lambda : None)()
            if o is None and sort_key == 'getObjPositionInParent':
                return getObjPositionInParent(obj)
            return o
        except TypeError:
            return

        return

    sorted_lst = sorted(lst, key=_get_sorted_key)
    if order == 'reverse' or order == 'descending':
        return list(reversed(sorted_lst))
    else:
        return sorted_lst


def getSortedSecureRefs(self, relationship=None, targetObject=None, sort_key=None, order='ascending'):
    """sorted get all the referenced objects for this object"""
    lst = self.getSecureRefs(relationship, targetObject)
    return _get_sorted_lst(lst, sort_key, order)


def getSortedSecureBRefs(self, relationship=None, targetObject=None, sort_key=None, order='ascending'):
    """sorted get all the back referenced objects for this object"""
    lst = self.getSecureBRefs(relationship, targetObject)
    return _get_sorted_lst(lst, sort_key, order)


Referenceable.getSecureRefs = getSecureRefs
info('adding method %s', str(Referenceable.getSecureRefs))
Referenceable.getSecureBRefs = getSecureBRefs
info('adding method %s', str(Referenceable.getSecureBRefs))
Referenceable.getSortedSecureRefs = getSortedSecureRefs
info('adding method %s', str(Referenceable.getSortedSecureRefs))
Referenceable.getSortedSecureBRefs = getSortedSecureBRefs
info('adding method %s', str(Referenceable.getSortedSecureBRefs))