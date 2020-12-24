# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_mission/migrations/0011_stageprize.py
# Compiled at: 2018-10-23 02:40:03
from __future__ import unicode_literals
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('bee_django_mission', '0010_userstage_prize_coin')]
    operations = [
     migrations.CreateModel(name=b'StagePrize', fields=[
      (
       b'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name=b'ID')),
      (
       b'coin', models.IntegerField(verbose_name=b'奖励M币')),
      (
       b'chance', models.FloatField(verbose_name=b'获得几率')),
      (
       b'stage', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=b'bee_django_mission.Stage', verbose_name=b'所属阶段'))], options={b'ordering': [
                    b'pk'], 
        b'db_table': b'bee_django_mission_stage_prize'})]