# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/maximsmirnov/.virtualenvs/django-antivirus-field/lib/python2.7/site-packages/django_antivirus_field/__init__.py
# Compiled at: 2014-10-16 06:13:40
from __future__ import unicode_literals
import sys, warnings
try:
    import django
except ImportError as err:
    warnings.warn((b'Cannot import django: {}').format(str(err)))
    sys.exit(1)

from django_antivirus_field.fields import ProtectedFileField
if django.VERSION[1] < 7:
    try:
        from south.modelsinspector import add_introspection_rules
        add_introspection_rules([], [b'^django_antivirus_field\\.fields\\.ProtectedFileField'])
    except Exception as err:
        warnings.warn((b'Problem with south: {}').format(str(err)))

__all__ = [
 b'ProtectedFileField']