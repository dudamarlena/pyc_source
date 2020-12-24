# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_mission/migrations/0012_auto_20181129_1444.py
# Compiled at: 2018-11-29 01:44:41
from __future__ import unicode_literals
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
     ('bee_django_mission', '0011_stageprize')]
    operations = [
     migrations.AlterModelOptions(name=b'line', options={b'ordering': [b'id'], b'permissions': (('can_manage_mission', '可以进入mission管理页'), )}),
     migrations.AlterModelOptions(name=b'missiontype', options={b'ordering': [b'id']}),
     migrations.AlterModelOptions(name=b'stage', options={b'ordering': [b'level']})]