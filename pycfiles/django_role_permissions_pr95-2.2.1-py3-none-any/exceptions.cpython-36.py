# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: f:\works\py\ipdiranproject\django-role-permissions\rolepermissions\exceptions.py
# Compiled at: 2018-12-20 13:42:50
# Size of source mod 2**32: 194 bytes
from __future__ import unicode_literals

class CheckerNotRegistered(Exception):
    pass


class RoleDoesNotExist(Exception):
    pass


class RolePermissionScopeException(Exception):
    pass