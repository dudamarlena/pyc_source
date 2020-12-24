# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/breno/Envs/djangoplus/lib/python3.7/site-packages/djangoplus/admin/migrations/0003_auto_20180416_1034.py
# Compiled at: 2018-10-05 12:53:01
# Size of source mod 2**32: 1405 bytes
from django.db import migrations

def migrate(apps, schema_editor):
    Organization = apps.get_model('admin', 'Organization')
    Unit = apps.get_model('admin', 'Unit')
    Scope = apps.get_model('admin', 'Scope')
    for i, scope in enumerate([Organization, Unit]):
        for cls in scope.__subclasses__():
            for obj in cls.objects.all():
                pk = obj.pk + 1000 * i
                Scope.objects.get_or_create(pk=pk)
                scope_lookup = {'id': obj.pk}
                scope_update = {'id': pk}
                ((scope.objects.filter)(**scope_lookup).update)(**scope_update)
                cls_lookup = {'{}_ptr_id'.format(scope.__name__.lower()): obj.pk}
                cls_update = {'{}_ptr_id'.format(scope.__name__.lower()): pk}
                ((cls.objects.filter)(**cls_lookup).update)(**cls_update)
                for rel in cls._meta.related_objects:
                    if rel.remote_field.model._meta.app_label == 'admin':
                        continue
                    lookup = {rel.remote_field.name: obj.pk}
                    update = {rel.remote_field.name: pk}
                    ((rel.remote_field.model.objects.filter)(**lookup).update)(**update)


class Migration(migrations.Migration):
    dependencies = [
     ('admin', '0002_scope')]
    operations = [
     migrations.RunPython(migrate)]