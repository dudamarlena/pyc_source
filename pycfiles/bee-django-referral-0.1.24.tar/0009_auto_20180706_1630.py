# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_referral/migrations/0009_auto_20180706_1630.py
# Compiled at: 2018-07-06 04:30:44
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('bee_django_referral', '0008_auto_20180706_1627')]
    operations = [
     migrations.AlterField(model_name=b'activity', name=b'show_type', field=models.IntegerField(choices=[(1, '全部显示'), (2, '指定用户显示')], default=1, verbose_name=b'显示类型'))]