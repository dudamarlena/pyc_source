# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_referral/migrations/0010_auto_20180708_1350.py
# Compiled at: 2018-07-08 01:50:41
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('bee_django_referral', '0009_auto_20180706_1630')]
    operations = [
     migrations.AlterField(model_name=b'activity', name=b'end_date', field=models.DateTimeField(blank=True, help_text=b'格式：2000-01-01 00:00:00', null=True, verbose_name=b'结束时间')),
     migrations.AlterField(model_name=b'activity', name=b'start_date', field=models.DateTimeField(blank=True, help_text=b'格式：2000-01-01 00:00:00', null=True, verbose_name=b'开始时间'))]