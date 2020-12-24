# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_crm/migrations/0008_preuser_pay_status.py
# Compiled at: 2018-08-23 04:56:37
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('bee_django_crm', '0007_auto_20180823_1533')]
    operations = [
     migrations.AddField(model_name=b'preuser', name=b'pay_status', field=models.IntegerField(choices=[(0, '未缴费'), (1, '全款缴清'), (2, '分期中')], default=0, verbose_name=b'缴费情况'))]