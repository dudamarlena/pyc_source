# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/security/indexer.py
# Compiled at: 2012-06-20 11:58:15
from zope.annotation.interfaces import IAnnotatable
from ztfy.security.interfaces import ILocalRoleManager, ISecurityManager, ILocalRoleIndexer
from zope.component import adapts
from zope.interface import implements
from zope.security.checker import CheckerPublic
from zope.security.proxy import removeSecurityProxy
ALL_ROLES_INDEX_NAME = 'all_roles'

class LocalRoleIndexer(object):
    """Local role indexer helper interface"""
    adapts(IAnnotatable)
    implements(ILocalRoleIndexer)

    def __init__(self, context):
        self.context = context

    __Security_checker__ = CheckerPublic

    def __getattr__(self, name):
        result = set()
        sm = ISecurityManager(self.context, None)
        if sm is None:
            return result
        else:
            if name == ALL_ROLES_INDEX_NAME:
                manager = ILocalRoleManager(self.context, None)
                if manager is None:
                    return result
                names = manager.__roles__
            else:
                names = (
                 name,)
            for name in names:
                result |= removeSecurityProxy(sm.getLocalAllowedPrincipals(name))

            return result