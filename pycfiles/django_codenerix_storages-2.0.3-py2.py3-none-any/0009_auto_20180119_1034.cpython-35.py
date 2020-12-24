# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/www.django/makarthy/codenerix_storages/migrations/0009_auto_20180119_1034.py
# Compiled at: 2018-01-19 04:34:17
# Size of source mod 2**32: 891 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('codenerix_storages', '0008_auto_20180119_1029')]
    operations = [
     migrations.RemoveField(model_name='inventory', name='closed'),
     migrations.RemoveField(model_name='inventory', name='opened'),
     migrations.AddField(model_name='inventory', name='end', field=models.DateTimeField(blank=True, null=True, verbose_name='End')),
     migrations.AddField(model_name='inventory', name='start', field=models.DateTimeField(blank=True, null=True, verbose_name='Start'))]