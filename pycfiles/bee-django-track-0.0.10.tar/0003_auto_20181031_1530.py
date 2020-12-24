# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_track/migrations/0003_auto_20181031_1530.py
# Compiled at: 2018-10-31 03:30:00
from __future__ import unicode_literals
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
     ('bee_django_track', '0002_auto_20180810_1846')]
    operations = [
     migrations.AlterModelOptions(name=b'usertrackrecord', options={b'ordering': [b'-created_at'], b'permissions': (('view_user_leave', '可以查看学生请假类足迹'), ('view_crm_fee', '可以查看缴费类足迹'), ('view_crm_referral', '可以查看转介类足迹'))})]