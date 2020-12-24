# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/cameron/Dev/kanban-dev/django-autotask/djautotask/migrations/0027_auto_20191125_1103.py
# Compiled at: 2019-11-28 19:04:27
# Size of source mod 2**32: 375 bytes
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
     ('djautotask', '0026_auto_20191125_0952')]
    operations = [
     migrations.RenameField(model_name='task',
       old_name='priority_label',
       new_name='priority')]