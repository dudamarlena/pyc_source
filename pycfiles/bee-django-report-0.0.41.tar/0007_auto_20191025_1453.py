# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_report/migrations/0007_auto_20191025_1453.py
# Compiled at: 2019-10-25 02:53:48
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('bee_django_report', '0006_auto_20190927_1449')]
    operations = [
     migrations.AddField(model_name=b'mentorscoreweek', name=b'score1', field=models.FloatField(blank=True, null=True, verbose_name=b'分数1')),
     migrations.AddField(model_name=b'mentorscoreweek', name=b'score2', field=models.FloatField(blank=True, null=True, verbose_name=b'分数2')),
     migrations.AddField(model_name=b'mentorscoreweek', name=b'score3', field=models.FloatField(blank=True, null=True, verbose_name=b'分数3')),
     migrations.AddField(model_name=b'mentorscoreweek', name=b'score4', field=models.FloatField(blank=True, null=True, verbose_name=b'分数4'))]