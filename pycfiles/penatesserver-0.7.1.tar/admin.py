# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mgallet/Github/Penates-Server/penatesserver/admin.py
# Compiled at: 2015-12-29 03:04:14
from django.contrib import admin
from penatesserver.models import Host, MountPoint, Service
__author__ = 'Matthieu Gallet'

class HostAdmin(admin.ModelAdmin):
    fields = (
     ('fqdn', 'owner'),
     ('main_ip_address', 'main_mac_address'),
     ('admin_ip_address', 'admin_mac_address'),
     ('serial', 'model_name', 'location'),
     ('os_name', 'bootp_filename'),
     ('proc_model', 'proc_count', 'core_count'),
     ('memory_size', 'disk_size'))
    list_display = ('fqdn', 'main_ip_address', 'admin_ip_address', 'serial', 'proc_count',
                    'core_count', 'memory_size', 'disk_size')
    ordering = ('fqdn', )
    search_fields = ('fqdn', 'serial', 'main_ip_address', 'admin_ip_address')


admin.site.register(Host, admin_class=HostAdmin)
admin.site.register(MountPoint)
admin.site.register(Service)