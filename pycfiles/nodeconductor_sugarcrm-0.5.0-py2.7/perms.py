# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/nodeconductor_sugarcrm/perms.py
# Compiled at: 2016-09-28 11:51:43
from nodeconductor.structure import perms as structure_perms
PERMISSION_LOGICS = (
 (
  'nodeconductor_sugarcrm.SugarCRMService', structure_perms.service_permission_logic),
 (
  'nodeconductor_sugarcrm.SugarCRMServiceProjectLink', structure_perms.service_project_link_permission_logic),
 (
  'nodeconductor_sugarcrm.CRM', structure_perms.resource_permission_logic))