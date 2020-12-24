# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/cameron/Dev/kanban-dev/django-autotask/djautotask/migrations/0058_auto_20200408_1022.py
# Compiled at: 2020-04-08 17:23:34
# Size of source mod 2**32: 717 bytes
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('djautotask', '0057_auto_20200406_1620')]
    operations = [
     migrations.AlterField(model_name='tasknote',
       name='publish',
       field=models.CharField(blank=True, choices=[(1, 'All Autotask Users'), (2, 'Internal Users')], max_length=20, null=True)),
     migrations.AlterField(model_name='ticketnote',
       name='publish',
       field=models.CharField(blank=True, choices=[(1, 'All Autotask Users'), (2, 'Internal Users')], max_length=20, null=True))]