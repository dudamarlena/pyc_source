# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/cameron/Dev/kanban-dev/django-autotask/djautotask/migrations/0013_auto_20190923_1439.py
# Compiled at: 2019-11-22 18:06:19
# Size of source mod 2**32: 446 bytes
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
     ('djautotask', '0012_merge_20190923_1439')]
    operations = [
     migrations.RemoveField(model_name='projectstatus',
       name='value'),
     migrations.RemoveField(model_name='projecttype',
       name='value')]