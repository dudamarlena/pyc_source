# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/www.django/makarthy/codenerix_storages/migrations/0010_auto_20180123_1316.py
# Compiled at: 2018-02-02 06:33:35
# Size of source mod 2**32: 685 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('codenerix_storages', '0009_auto_20180119_1034')]
    operations = [
     migrations.AlterField(model_name='inventory', name='end', field=models.DateTimeField(blank=True, null=True, verbose_name='Ends')),
     migrations.AlterField(model_name='inventory', name='start', field=models.DateTimeField(blank=True, null=True, verbose_name='Starts'))]