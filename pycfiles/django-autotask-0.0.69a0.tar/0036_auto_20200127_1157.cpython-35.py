# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/sam/git/Kanban/django-autotask/djautotask/migrations/0036_auto_20200127_1157.py
# Compiled at: 2020-01-29 14:01:52
# Size of source mod 2**32: 1456 bytes
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
     ('djautotask', '0035_timeentry')]
    operations = [
     migrations.RemoveField(model_name='displaycolor', name='parent_value'),
     migrations.RemoveField(model_name='issuetype', name='parent_value'),
     migrations.RemoveField(model_name='licensetype', name='parent_value'),
     migrations.RemoveField(model_name='priority', name='parent_value'),
     migrations.RemoveField(model_name='projectstatus', name='parent_value'),
     migrations.RemoveField(model_name='projecttype', name='parent_value'),
     migrations.RemoveField(model_name='queue', name='parent_value'),
     migrations.RemoveField(model_name='source', name='parent_value'),
     migrations.RemoveField(model_name='status', name='parent_value'),
     migrations.RemoveField(model_name='subissuetype', name='parent_value'),
     migrations.RemoveField(model_name='tickettype', name='parent_value')]