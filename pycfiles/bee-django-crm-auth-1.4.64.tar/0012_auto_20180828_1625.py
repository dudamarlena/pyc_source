# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_crm/migrations/0012_auto_20180828_1625.py
# Compiled at: 2018-08-28 04:25:53
from __future__ import unicode_literals
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
     ('bee_django_crm', '0011_auto_20180828_1556')]
    operations = [
     migrations.AlterModelOptions(name=b'preuserfee', options={b'ordering': [b'-paid_at', b'-created_at'], b'permissions': (('view_crm_preuser_fee', '可以查看用户缴费'), ('can_check_crm_preuser_fee', '可以审核用户缴费'), ('can_after_checked_fee', '审核缴费后可以后续操作'))})]