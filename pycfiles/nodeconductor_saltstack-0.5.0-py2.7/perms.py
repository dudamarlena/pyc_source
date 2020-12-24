# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/nodeconductor_saltstack/sharepoint/perms.py
# Compiled at: 2016-09-28 02:05:53
from nodeconductor.core.permissions import StaffPermissionLogic
from nodeconductor.structure import perms as structure_perms
from ..saltstack.perms import property_permission_logic
PERMISSION_LOGICS = (
 (
  'sharepoint.SharepointTenant', structure_perms.resource_permission_logic),
 (
  'sharepoint.Template', StaffPermissionLogic(any_permission=True)),
 (
  'sharepoint.User', property_permission_logic),
 (
  'sharepoint.SiteCollection', property_permission_logic))