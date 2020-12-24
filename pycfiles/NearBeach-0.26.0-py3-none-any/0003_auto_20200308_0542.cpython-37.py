# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/luke/PycharmProjects/untitled1/NearBeach/migrations/0003_auto_20200308_0542.py
# Compiled at: 2020-03-27 20:27:18
# Size of source mod 2**32: 881 bytes
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('NearBeach', '0002_initialise_data')]
    operations = [
     migrations.RemoveField(model_name='project_task',
       name='change_user'),
     migrations.RemoveField(model_name='project_task',
       name='project_id'),
     migrations.RemoveField(model_name='project_task',
       name='task_id'),
     migrations.AddField(model_name='kanban_board',
       name='kanban_board_status',
       field=models.CharField(choices=[('Open', 'Open'), ('Closed', 'Closed')], default='Open', max_length=10)),
     migrations.DeleteModel(name='project_task')]