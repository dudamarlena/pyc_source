# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/robertbanagale/code/opensource/django-address/django-address/example_site/address/compat.py
# Compiled at: 2020-05-10 01:24:31
import django
from django.db.models.fields.related import ForeignObject
django_version = django.VERSION
is_django2 = django_version >= (2, 0)

def compat_contribute_to_class(self, cls, name, virtual_only=False):
    if is_django2:
        super(ForeignObject, self).contribute_to_class(cls, name, private_only=virtual_only)
    else:
        super(ForeignObject, self).contribute_to_class(cls, name, virtual_only=virtual_only)