# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_track/migrations/0006_auto_20181109_1336.py
# Compiled at: 2018-11-09 00:36:17
from __future__ import unicode_literals
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
     ('bee_django_track', '0005_auto_20181031_1534')]
    operations = [
     migrations.AlterModelOptions(name=b'usertrackrecord', options={b'ordering': [b'-created_at'], b'permissions': (('add_track_other', '可以添加其他类足迹'), ('view_track_other', '可以查看其他类足迹'))})]