# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_crm/migrations/0034_auto_20191128_1411.py
# Compiled at: 2019-11-28 01:11:51
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('bee_django_crm', '0033_auto_20191128_1312')]
    operations = [
     migrations.AlterField(model_name=b'campaignrecord', name=b'count', field=models.IntegerField(default=0, verbose_name=b'砍价次数')),
     migrations.AlterField(model_name=b'campaignrecord', name=b'result', field=models.FloatField(default=0, verbose_name=b'砍价结果'))]