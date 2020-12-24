# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/nodeconductor_zabbix/apps.py
# Compiled at: 2016-09-21 16:06:28
from __future__ import unicode_literals
from django.apps import AppConfig
from django.db.models import signals
from django_fsm import signals as fsm_signals

class ZabbixConfig(AppConfig):
    name = b'nodeconductor_zabbix'
    verbose_name = b'NodeConductor Zabbix'
    service_name = b'Zabbix'

    def ready(self):
        from nodeconductor.structure import SupportedServices, models as structure_models
        from .backend import ZabbixBackend
        SupportedServices.register_backend(ZabbixBackend)
        from . import handlers
        for index, resource_model in enumerate(structure_models.ResourceMixin.get_all_models()):
            fsm_signals.post_transition.connect(handlers.delete_hosts_on_scope_deletion, sender=resource_model, dispatch_uid=b'nodeconductor_zabbix.handlers.delete_hosts_on_scope_deletion_%s_%s' % (
             index, resource_model.__name__))

        signals.post_save.connect(handlers.refresh_database_connection, sender=structure_models.ServiceSettings, dispatch_uid=b'nodeconductor_zabbix.handlers.refresh_database_connection')