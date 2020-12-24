# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_referral/migrations/0012_auto_20190821_1315.py
# Compiled at: 2019-08-21 01:15:54
from __future__ import unicode_literals
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
     ('bee_django_referral', '0011_activity_link')]
    operations = [
     migrations.AlterModelOptions(name=b'activity', options={b'permissions': (('can_manage_referral', '可以进入转介活动管理页'), )})]