# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_mission/migrations/0015_auto_20181219_2057.py
# Compiled at: 2018-12-19 07:57:46
from __future__ import unicode_literals
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
     ('bee_django_mission', '0014_auto_20181130_1533')]
    operations = [
     migrations.AlterModelOptions(name=b'mission', options={b'ordering': [b'created_at'], b'permissions': (('view_mission_list', '查看任务列表'), )}),
     migrations.AlterModelOptions(name=b'stage', options={b'ordering': [b'level'], b'permissions': (('view_stage_list', '查看阶段列表'), )})]