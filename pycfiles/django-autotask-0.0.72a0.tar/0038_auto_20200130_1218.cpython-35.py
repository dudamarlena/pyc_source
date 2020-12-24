# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/sam/git/Kanban/django-autotask/djautotask/migrations/0038_auto_20200130_1218.py
# Compiled at: 2020-01-31 18:17:22
# Size of source mod 2**32: 416 bytes
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
     ('djautotask', '0037_subissuetype_parent_value')]
    operations = [
     migrations.AlterModelOptions(name='timeentry', options={'ordering': ('-start_date_time', 'id'), 'verbose_name_plural': 'Time entries'})]