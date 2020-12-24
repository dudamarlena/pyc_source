# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/nodeconductor_paas_oracle/perms.py
# Compiled at: 2016-12-16 07:39:01
from nodeconductor.core.permissions import StaffPermissionLogic
from nodeconductor.structure import perms as structure_perms
PERMISSION_LOGICS = (
 (
  'nodeconductor_paas_oracle.OracleService', structure_perms.service_permission_logic),
 (
  'nodeconductor_paas_oracle.OracleServiceProjectLink', structure_perms.service_project_link_permission_logic),
 (
  'nodeconductor_paas_oracle.Deployment', structure_perms.resource_permission_logic),
 (
  'nodeconductor_paas_oracle.Flavor', StaffPermissionLogic(any_permission=True)))