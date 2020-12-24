# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/sam/git/Kanban/django-autotask/djautotask/migrations/0010_auto_20190923_0930.py
# Compiled at: 2019-10-01 19:08:49
# Size of source mod 2**32: 1036 bytes
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('djautotask', '0009_auto_20190918_1525')]
    operations = [
     migrations.RemoveField(model_name='project', name='completed_date_time'),
     migrations.RemoveField(model_name='project', name='end_date_time'),
     migrations.RemoveField(model_name='project', name='start_date_time'),
     migrations.AddField(model_name='project', name='completed_date', field=models.DateField(null=True)),
     migrations.AddField(model_name='project', name='end_date', field=models.DateField(null=True)),
     migrations.AddField(model_name='project', name='start_date', field=models.DateField(null=True))]