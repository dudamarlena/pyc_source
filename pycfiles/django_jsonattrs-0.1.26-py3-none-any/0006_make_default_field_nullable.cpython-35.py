# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Volumes/Work/dev/cadasta/django-jsonattrs/jsonattrs/migrations/0006_make_default_field_nullable.py
# Compiled at: 2017-04-11 03:59:22
# Size of source mod 2**32: 485 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('jsonattrs', '0005_remove_monolingual_fields')]
    operations = [
     migrations.AlterField(model_name='attribute', name='default', field=models.CharField(blank=True, max_length=256, null=True))]