# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_crm/migrations/0047_auto_20191226_1354.py
# Compiled at: 2019-12-26 00:54:45
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('bee_django_crm', '0046_auto_20191225_1736')]
    operations = [
     migrations.AddField(model_name=b'bargainreward', name=b'end_money', field=models.FloatField(blank=True, null=True, verbose_name=b'完成金额')),
     migrations.AddField(model_name=b'bargainreward', name=b'end_time', field=models.DateTimeField(blank=True, null=True, verbose_name=b'活动结束时间')),
     migrations.AddField(model_name=b'bargainreward', name=b'max_bargain', field=models.IntegerField(default=1, verbose_name=b'最大砍价次数')),
     migrations.AddField(model_name=b'bargainreward', name=b'start_money', field=models.FloatField(blank=True, null=True, verbose_name=b'起始金额')),
     migrations.AddField(model_name=b'bargainreward', name=b'start_time', field=models.DateTimeField(blank=True, null=True, verbose_name=b'活动开始时间'))]