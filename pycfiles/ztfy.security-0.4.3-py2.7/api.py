# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/security/tal/api.py
# Compiled at: 2012-06-20 11:58:16
__docformat__ = 'restructuredtext'
from zope.tales.interfaces import ITALESFunctionNamespace
from ztfy.security.tal.interfaces import ISecurityPermissionTalesAPI
from zope.interface import implements
from ztfy.security.security import getSecurityManager

class SecurityPermissionTalesAdapter(object):
    """Security permission TALES adapter"""
    implements(ISecurityPermissionTalesAPI, ITALESFunctionNamespace)

    def __init__(self, context):
        self.context = context
        self.sm = getSecurityManager(context)

    def setEngine(self, engine):
        self.request = engine.vars['request']

    def __getattr__(self, permission):
        if self.sm is None:
            return False
        else:
            return self.sm.canUsePermission(permission)