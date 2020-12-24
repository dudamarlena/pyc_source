# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/nodeconductor_zabbix/urls.py
# Compiled at: 2016-09-21 16:06:28
from . import views

def register_in(router):
    router.register('zabbix', views.ZabbixServiceViewSet, base_name='zabbix')
    router.register('zabbix-hosts', views.HostViewSet, base_name='zabbix-host')
    router.register('zabbix-itservices', views.ITServiceViewSet, base_name='zabbix-itservice')
    router.register('zabbix-service-project-link', views.ZabbixServiceProjectLinkViewSet, base_name='zabbix-spl')
    router.register('zabbix-templates', views.TemplateViewSet, base_name='zabbix-template')
    router.register('zabbix-triggers', views.TriggerViewSet, base_name='zabbix-trigger')
    router.register('zabbix-user-groups', views.UserGroupViewSet, base_name='zabbix-user-group')
    router.register('zabbix-users', views.UserViewSet, base_name='zabbix-user')