# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/s.lihobabin/projects/protector/django-protector/protector/migrations/0006_auto_20180726_1229.py
# Compiled at: 2019-05-29 13:12:49
# Size of source mod 2**32: 1076 bytes
from __future__ import unicode_literals
from django.db import migrations

def forwards_func(apps, schema_editor):
    OwnerToPermission = apps.get_model('protector', 'OwnerToPermission')
    OwnerToPermission.objects.filter(content_type_id=1,
      object_id=0).update(content_type=None,
      object_id=None)


def backwards_func(apps, schema_editor):
    OwnerToPermission = apps.get_model('protector', 'OwnerToPermission')
    OwnerToPermission.objects.filter(content_type_id__isnull=True,
      object_id__isnull=True).update(content_type_id=1,
      object_id=0)


class Migration(migrations.Migration):
    dependencies = [
     ('protector', '0005_auto_20180725_1629')]
    operations = [
     migrations.RunPython(forwards_func, backwards_func)]