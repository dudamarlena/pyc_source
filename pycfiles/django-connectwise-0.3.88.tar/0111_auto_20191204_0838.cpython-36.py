# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/cameron/Dev/kanban-dev/django-connectwise/djconnectwise/migrations/0111_auto_20191204_0838.py
# Compiled at: 2019-12-04 18:58:20
# Size of source mod 2**32: 549 bytes
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
     ('djconnectwise', '0110_project_company')]
    operations = [
     migrations.RenameField(model_name='scheduleentry',
       old_name='expected_date_end',
       new_name='date_end'),
     migrations.RenameField(model_name='scheduleentry',
       old_name='expected_date_start',
       new_name='date_start')]