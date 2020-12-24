# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/nodeconductor_killbill/perms.py
# Compiled at: 2016-09-25 09:47:37
from nodeconductor.core.permissions import FilteredCollaboratorsPermissionLogic
from nodeconductor.structure import models as structure_models
PERMISSION_LOGICS = (
 (
  'nodeconductor_killbill.Invoice',
  FilteredCollaboratorsPermissionLogic(collaborators_query='customer__roles__permission_group__user', collaborators_filter={'customer__roles__role_type': structure_models.CustomerRole.OWNER}, any_permission=True)),)