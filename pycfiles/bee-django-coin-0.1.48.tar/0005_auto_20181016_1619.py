# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_coin/migrations/0005_auto_20181016_1619.py
# Compiled at: 2018-10-16 04:19:04
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('bee_django_coin', '0004_auto_20180620_1845')]
    operations = [
     migrations.CreateModel(name=b'OtherCoinCount', fields=[
      (
       b'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name=b'ID')),
      (
       b'other_type', models.CharField(choices=[(1, '班级剩余金币')], max_length=180, null=True)),
      (
       b'other_type_id', models.IntegerField()),
      (
       b'count', models.IntegerField(default=0)),
      (
       b'update_at', models.DateTimeField(auto_now=True))], options={b'ordering': [
                    b'pk'], 
        b'db_table': b'bee_django_coin_other_count'}),
     migrations.AddField(model_name=b'usercoinrecord', name=b'coin_content_id', field=models.IntegerField(null=True))]