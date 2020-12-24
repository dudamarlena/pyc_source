# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_report/migrations/0008_auto_20191025_1640.py
# Compiled at: 2019-10-25 04:40:29
from __future__ import unicode_literals
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
     ('bee_django_report', '0007_auto_20191025_1453')]
    operations = [
     migrations.AlterModelOptions(name=b'mentorscoreweek', options={b'ordering': [b'created_at'], b'permissions': (('view_mentorscoreweek', '可以查看全部助教分数'), ('change_score1', '可以修改分数1'), ('change_score2', '可以修改分数2'), ('change_score3', '可以修改分数3'), ('change_score4', '可以修改分数4'))})]