# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_report/migrations/0006_auto_20190927_1449.py
# Compiled at: 2019-09-27 02:49:13
from __future__ import unicode_literals
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
     ('bee_django_report', '0005_auto_20190830_1413')]
    operations = [
     migrations.AlterModelOptions(name=b'mentorscoreweek', options={b'ordering': [b'created_at'], b'permissions': (('view_mentorscoreweek', '可以查看全部助教分数'), )}),
     migrations.AlterModelOptions(name=b'report', options={b'permissions': (('can_view_report', '可以查看报表'), )})]