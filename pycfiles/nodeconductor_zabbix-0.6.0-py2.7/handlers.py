# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/nodeconductor_zabbix/handlers.py
# Compiled at: 2016-09-21 16:06:28
import logging
from nodeconductor.structure.models import Resource
from . import executors
from .models import Host
logger = logging.getLogger(__name__)

def delete_hosts_on_scope_deletion(sender, instance, name, source, target, **kwargs):
    if target != Resource.States.DELETING:
        return
    for host in Host.objects.filter(scope=instance):
        if host.state == Host.States.OK:
            executors.HostDeleteExecutor.execute(host)
        elif host.state == Host.States.ERRED:
            executors.HostDeleteExecutor.execute(host, force=True)
        else:
            logger.exception('Instance %s host was in state %s on instance deletion.', instance, host.human_readable_state)
            host.set_erred()
            host.save()
            executors.HostDeleteExecutor.execute(host, force=True)


def refresh_database_connection(sender, instance, created=False, **kwargs):
    if not created and instance.type == 'Zabbix' and instance.tracker.has_changed('options'):
        instance.get_backend()._get_db_connection(force=True)