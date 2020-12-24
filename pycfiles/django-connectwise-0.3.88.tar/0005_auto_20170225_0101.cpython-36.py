# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/cameron/Dev/kanban-dev/django-connectwise/djconnectwise/migrations/0005_auto_20170225_0101.py
# Compiled at: 2019-05-14 12:25:52
# Size of source mod 2**32: 732 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('djconnectwise', '0004_auto_20170224_1853')]
    operations = [
     migrations.RenameField(model_name='callbackentry',
       old_name='enabled',
       new_name='inactive_flag'),
     migrations.RemoveField(model_name='callbackentry',
       name='entry_id'),
     migrations.AddField(model_name='callbackentry',
       name='description',
       field=models.CharField(max_length=100, default=''),
       preserve_default=False)]