# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/cameron/Dev/kanban-dev/django-connectwise/djconnectwise/migrations/0006_auto_20170303_1242.py
# Compiled at: 2019-05-14 12:25:52
# Size of source mod 2**32: 444 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('djconnectwise', '0005_auto_20170225_0101')]
    operations = [
     migrations.AlterField(model_name='callbackentry',
       name='description',
       field=models.CharField(max_length=100, null=True, blank=True))]