# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-jkXn_D/South/south/introspection_plugins/django_objectpermissions.py
# Compiled at: 2018-07-11 18:15:31
"""
South introspection rules for django-objectpermissions
"""
from django.conf import settings
from south.modelsinspector import add_ignored_fields
if 'objectpermissions' in settings.INSTALLED_APPS:
    try:
        from objectpermissions.models import UserPermissionRelation, GroupPermissionRelation
    except ImportError:
        pass
    else:
        add_ignored_fields(['^objectpermissions\\.models\\.UserPermissionRelation',
         '^objectpermissions\\.models\\.GroupPermissionRelation'])