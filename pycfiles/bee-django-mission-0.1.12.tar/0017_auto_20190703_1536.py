# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_mission/migrations/0017_auto_20190703_1536.py
# Compiled at: 2019-07-03 04:15:37
from __future__ import unicode_literals
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
     ('bee_django_mission', '0016_userstage_token')]
    operations = [
     migrations.AlterModelOptions(name=b'line', options={b'ordering': [b'id'], b'permissions': (('can_manage_mission', '可以进入mission管理页'), ('view_index_mission', '可以进入首页任务板块'))})]