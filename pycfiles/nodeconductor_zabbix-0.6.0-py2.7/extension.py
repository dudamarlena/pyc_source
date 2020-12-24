# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/nodeconductor_zabbix/extension.py
# Compiled at: 2016-09-21 16:06:28
from nodeconductor.core import NodeConductorExtension

class ZabbixExtension(NodeConductorExtension):

    class Settings:
        NODECONDUCTOR_ZABBIX = {'SMS_SETTINGS': {'SMS_EMAIL_FROM': None, 
                            'SMS_EMAIL_RCPT': None}}

    @staticmethod
    def django_app():
        return 'nodeconductor_zabbix'

    @staticmethod
    def rest_urls():
        from .urls import register_in
        return register_in

    @staticmethod
    def celery_tasks():
        from datetime import timedelta
        return {'update-monthly-slas': {'task': 'nodeconductor.zabbix.update_sla', 
                                   'schedule': timedelta(minutes=5), 
                                   'args': ('monthly', )}, 
           'update-yearly-slas': {'task': 'nodeconductor.zabbix.update_sla', 
                                  'schedule': timedelta(minutes=10), 
                                  'args': ('yearly', )}, 
           'update-monitoring-items': {'task': 'nodeconductor.zabbix.update_monitoring_items', 
                                       'schedule': timedelta(minutes=10)}, 
           'pull-zabbix-hosts': {'task': 'nodeconductor.zabbix.pull_hosts', 
                                 'schedule': timedelta(minutes=30)}}