# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dmeliza/Devel/django-neurobank/neurobank/migrations/0002_auto_20170624_0926.py
# Compiled at: 2017-06-24 09:26:41
# Size of source mod 2**32: 1399 bytes
from __future__ import unicode_literals
import django.contrib.postgres.fields.hstore
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('neurobank', '0001_initial')]
    operations = [
     migrations.RemoveField(model_name='domain', name='url'),
     migrations.AddField(model_name='domain', name='method', field=models.CharField(default='file://', help_text='Protocol for accessing resources in this domain.Use standard url notation (e.g., http:// or file://)', max_length=16), preserve_default=False),
     migrations.AddField(model_name='domain', name='root', field=models.CharField(default='', help_text='Root path for resources. Include authority for remote resources', max_length=512), preserve_default=False),
     migrations.AlterField(model_name='domain', name='name', field=models.CharField(help_text='A descriptive name', max_length=32)),
     migrations.AlterField(model_name='resource', name='metadata', field=django.contrib.postgres.fields.hstore.HStoreField(blank=True))]