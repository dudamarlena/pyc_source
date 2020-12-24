# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Volumes/Work/dev/cadasta/django-jsonattrs/jsonattrs/migrations/0002_attribute_choice_labels.py
# Compiled at: 2017-01-30 12:18:04
# Size of source mod 2**32: 562 bytes
from __future__ import unicode_literals
import django.contrib.postgres.fields
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('jsonattrs', '0001_initial')]
    operations = [
     migrations.AddField(model_name='attribute', name='choice_labels', field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=512), null=True, size=None))]