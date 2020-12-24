# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_mission/migrations/0005_auto_20180605_1631.py
# Compiled at: 2018-06-14 06:29:04
from __future__ import unicode_literals
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
     ('bee_django_mission', '0004_missiontype_line_type')]
    operations = [
     migrations.AlterModelOptions(name=b'usermission', options={b'ordering': [b'finish_at'], b'permissions': (('can_reset_user_mission', '可以重置学生的任务'), ), b'verbose_name': b'学生的任务'})]