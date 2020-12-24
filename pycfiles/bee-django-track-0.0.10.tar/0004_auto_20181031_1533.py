# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_track/migrations/0004_auto_20181031_1533.py
# Compiled at: 2018-10-31 03:33:28
from __future__ import unicode_literals
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
     ('bee_django_track', '0003_auto_20181031_1530')]
    operations = [
     migrations.AlterModelOptions(name=b'usertrackrecord', options={b'ordering': [b'-created_at'], b'permissions': (('add_user_leave', '可以添加学生请假类足迹'), ('view_user_leave', '可以查看学生请假类足迹'), ('add_crm_fee', '可以添加缴费类足迹'), ('view_crm_fee', '可以查看缴费类足迹'), ('add_crm_referral', '可以添加转介类足迹'), ('view_crm_referral', '可以查看转介类足迹'), ('add_track_other', '可以添加其他类足迹'), ('view_track_other', '可以查看其他类足迹'))})]