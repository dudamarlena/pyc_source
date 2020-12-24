# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/filipeximenes/Projects/django-role-permissions/rolepermissions/apps.py
# Compiled at: 2018-12-02 06:53:46
# Size of source mod 2**32: 267 bytes
from django.apps import AppConfig
from rolepermissions.loader import load_roles_and_permissions

class RolePermissions(AppConfig):
    name = 'rolepermissions'
    verbose_name = 'Django Role Permissions'

    def ready(self):
        load_roles_and_permissions()