# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Volumes/Work/dev/cadasta/django-jsonattrs/jsonattrs/migrations/0003_prepare_multilingual_setup.py
# Compiled at: 2017-01-30 12:18:04
# Size of source mod 2**32: 982 bytes
from __future__ import unicode_literals
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.migrations.operations.special

class Migration(migrations.Migration):
    dependencies = [
     ('jsonattrs', '0002_attribute_choice_labels')]
    operations = [
     migrations.AddField(model_name='attribute', name='choice_labels_xlat', field=django.contrib.postgres.fields.jsonb.JSONField(null=True)),
     migrations.AddField(model_name='attribute', name='long_name_xlat', field=django.contrib.postgres.fields.jsonb.JSONField(default={}), preserve_default=False),
     migrations.AddField(model_name='schema', name='default_language', field=models.CharField(blank=True, max_length=3))]