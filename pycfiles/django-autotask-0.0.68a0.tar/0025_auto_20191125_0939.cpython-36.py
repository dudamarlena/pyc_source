# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/cameron/Dev/kanban-dev/django-autotask/djautotask/migrations/0025_auto_20191125_0939.py
# Compiled at: 2019-11-26 15:02:19
# Size of source mod 2**32: 362 bytes
from django.db import migrations

class Migration(migrations.Migration):
    atomic = False
    dependencies = [
     ('djautotask', '0024_auto_20191122_1516')]
    operations = [
     migrations.RenameModel(old_name='TicketPriority',
       new_name='Priority')]