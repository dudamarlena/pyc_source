# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_crm/migrations/0033_auto_20191128_1312.py
# Compiled at: 2019-11-28 00:12:58
from __future__ import unicode_literals
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('bee_django_crm', '0032_auto_20191127_1721')]
    operations = [
     migrations.CreateModel(name=b'BargainRecord', fields=[
      (
       b'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name=b'ID')),
      (
       b'result', models.FloatField(verbose_name=b'砍价结果')),
      (
       b'created_at', models.DateTimeField(auto_now_add=True))], options={b'db_table': b'bee_django_crm_bargain_record'}),
     migrations.CreateModel(name=b'BargainReward', fields=[
      (
       b'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name=b'ID')),
      (
       b'title', models.CharField(max_length=180, verbose_name=b'奖励名称'))], options={b'db_table': b'bee_django_bargain_reward'}),
     migrations.CreateModel(name=b'CampaignRecord', fields=[
      (
       b'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name=b'ID')),
      (
       b'count', models.IntegerField(verbose_name=b'砍价次数')),
      (
       b'result', models.FloatField(verbose_name=b'砍价结果')),
      (
       b'status', models.IntegerField(choices=[(1, '进行中'), (2, '已提取')], default=1)),
      (
       b'created_at', models.DateTimeField(auto_now_add=True)),
      (
       b'reward', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=b'bee_django_crm.BargainReward', verbose_name=b'奖品')),
      (
       b'wxuser', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=b'bee_django_crm.WXUser', verbose_name=b'微信用户'))], options={b'db_table': b'bee_django_crm_bargain_campaign_record'}),
     migrations.AddField(model_name=b'bargainrecord', name=b'campaign_record', field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=b'bee_django_crm.CampaignRecord', verbose_name=b'参与记录')),
     migrations.AddField(model_name=b'bargainrecord', name=b'op_wxuser', field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name=b'op_wxuser', to=b'bee_django_crm.WXUser', verbose_name=b'助力的微信用户'))]