# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyams_security/index.py
# Compiled at: 2020-02-21 07:52:38
# Size of source mod 2**32: 1089 bytes
"""PyAMS_security.index module

"""
from hypatia.keyword import KeywordIndex
from pyams_security.interfaces import IProtectedObject
__docformat__ = 'restructuredtext'

class PrincipalsRoleIndex(KeywordIndex):
    __doc__ = 'Principals role index'

    def __init__(self, role_id, family=None):
        KeywordIndex.__init__(self, role_id, family)
        self.role_id = role_id

    def discriminate(self, obj, default):
        protected_object = IProtectedObject(obj, None)
        if protected_object is None:
            return default
        return protected_object.get_principals(self.role_id)