# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-jkXn_D/South/south/introspection_plugins/django_audit_log.py
# Compiled at: 2018-07-11 18:15:31
"""                                                 
South introspection rules for django-audit-log
"""
from django.contrib.auth.models import User
from django.conf import settings
from south.modelsinspector import add_introspection_rules
if 'audit_log' in settings.INSTALLED_APPS:
    try:
        from audit_log.models import fields
        rules = [
         (
          (
           fields.LastUserField,), [],
          {'to': [
                  'rel.to', {'default': User}], 
             'null': [
                    'null', {'default': True}]})]
        add_introspection_rules(rules, [
         '^audit_log\\.models\\.fields\\.LastUserField'])
    except ImportError:
        pass