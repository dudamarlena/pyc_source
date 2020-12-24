# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dmeliza/Devel/django-neurobank/neurobank/migrations/0003_auto_20170624_0933.py
# Compiled at: 2017-06-24 09:33:25
# Size of source mod 2**32: 979 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('neurobank', '0002_auto_20170624_0926')]
    operations = [
     migrations.RemoveField(model_name='domain', name='method'),
     migrations.RemoveField(model_name='domain', name='root'),
     migrations.AddField(model_name='domain', name='remote', field=models.BooleanField(default=False), preserve_default=False),
     migrations.AddField(model_name='domain', name='url', field=models.CharField(default='', help_text='Root path for resources. Include method and authority for remote resources', max_length=512), preserve_default=False)]