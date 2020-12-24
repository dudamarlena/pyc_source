# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/cameron/Dev/kanban-dev/django-autotask/djautotask/migrations/0050_remove_ticket_role.py
# Compiled at: 2020-02-28 16:41:52
# Size of source mod 2**32: 331 bytes
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
     ('djautotask', '0049_merge_20200227_1701')]
    operations = [
     migrations.RemoveField(model_name='ticket',
       name='role')]