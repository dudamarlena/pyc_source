# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-n_sfyb/Django/django/contrib/contenttypes/migrations/0002_remove_content_type_name.py
# Compiled at: 2019-02-14 00:35:16
from __future__ import unicode_literals
from django.db import migrations, models

def add_legacy_name(apps, schema_editor):
    ContentType = apps.get_model(b'contenttypes', b'ContentType')
    for ct in ContentType.objects.all():
        try:
            ct.name = apps.get_model(ct.app_label, ct.model)._meta.object_name
        except LookupError:
            ct.name = ct.model

        ct.save()


class Migration(migrations.Migration):
    dependencies = [
     ('contenttypes', '0001_initial')]
    operations = [
     migrations.AlterModelOptions(name=b'contenttype', options={b'verbose_name': b'content type', b'verbose_name_plural': b'content types'}),
     migrations.AlterField(model_name=b'contenttype', name=b'name', field=models.CharField(max_length=100, null=True)),
     migrations.RunPython(migrations.RunPython.noop, add_legacy_name, hints={b'model_name': b'contenttype'}),
     migrations.RemoveField(model_name=b'contenttype', name=b'name')]