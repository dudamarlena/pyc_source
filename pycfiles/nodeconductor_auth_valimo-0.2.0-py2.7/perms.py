# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/nodeconductor_auth_valimo/perms.py
# Compiled at: 2016-09-19 07:37:17
from nodeconductor.core.permissions import StaffPermissionLogic
PERMISSION_LOGICS = (
 (
  'nodeconductor_auth_valimo.AuthResult', StaffPermissionLogic(any_permission=True)),)