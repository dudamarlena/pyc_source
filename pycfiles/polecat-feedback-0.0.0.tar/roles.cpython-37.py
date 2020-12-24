# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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