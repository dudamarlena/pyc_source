# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/sam/git/Kanban/django-autotask/djautotask/migrations/0023_auto_20191119_0923.py
# Compiled at: 2019-11-19 14:09:33
# Size of source mod 2**32: 401 bytes
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('djautotask', '0022_merge_20191031_1620')]
    operations = [
     migrations.AlterField(model_name='project', name='duration', field=models.PositiveIntegerField(default=0))]