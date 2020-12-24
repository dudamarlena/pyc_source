# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/bouma/gitprojects/provgroningen/buildout/src/djinn_auth/djinn_auth/models/globalrole.py
# Compiled at: 2014-12-08 06:02:47
from djinn_auth.models.base import RoleAssignment

class GlobalRole(RoleAssignment):
    """Provide a means of giving a user or group a specific role that
    is global, so it will add it's permissions on ALL calls on for
    instance 'has_perm'.

    """

    class Meta:
        app_label = 'djinn_auth'