# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python3.7/site-packages/polecat_auth/roles.py
# Compiled at: 2019-07-25 22:51:52
# Size of source mod 2**32: 234 bytes
from polecat import model
__all__ = ('AdminRole', 'UserRole', 'DefaultRole')

class AdminRole(model.Role):
    pass


class UserRole(model.Role):
    parents = (
     AdminRole,)


class DefaultRole(model.Role):
    parents = (
     UserRole,)