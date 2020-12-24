# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyams_security/index.py
# Compiled at: 2020-02-21 07:52:38
# Size of source mod 2**32: 1089 bytes
__doc__ = 'PyAMS_security.index module\n\n'
from hypatia.keyword import KeywordIndex
from pyams_security.interfaces import IProtectedObject
__docformat__ = 'restructuredtext'

class PrincipalsRoleIndex(KeywordIndex):
    """PrincipalsRoleIndex"""

    def __init__(self, role_id, family=None):
        KeywordIndex.__init__(self, role_id, family)
        self.role_id = role_id

    def discriminate(self, obj, default):
        protected_object = IProtectedObject(obj, None)
        if protected_object is None:
            return default
        return protected_object.get_principals(self.role_id)