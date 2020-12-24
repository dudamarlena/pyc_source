# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/nodeconductor_organization/apps.py
# Compiled at: 2016-09-25 10:50:25
from __future__ import unicode_literals
from django.apps import AppConfig
from django.db.models import signals
from nodeconductor_organization import handlers

class OrganizationConfig(AppConfig):
    name = b'nodeconductor_organization'
    verbose_name = b'NodeConductor Organization'

    def ready(self):
        OrganizationUser = self.get_model(b'OrganizationUser')
        signals.post_save.connect(handlers.log_organization_user_save, sender=OrganizationUser, dispatch_uid=b'nodeconductor_organization.handlers.log_organization_user_save')
        signals.post_delete.connect(handlers.log_organization_user_delete, sender=OrganizationUser, dispatch_uid=b'nodeconductor_organization.handlers.log_organization_user_delete')