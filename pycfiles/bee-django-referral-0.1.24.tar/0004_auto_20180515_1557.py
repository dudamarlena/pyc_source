# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_referral/migrations/0004_auto_20180515_1557.py
# Compiled at: 2018-06-14 06:29:04
from __future__ import unicode_literals
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('bee_django_referral', '0003_auto_20180514_1812')]
    operations = [
     migrations.CreateModel(name=b'UserShareImageRecord', fields=[
      (
       b'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name=b'ID')),
      (
       b'preuser_id', models.IntegerField(verbose_name=b'crm中preuser的id')),
      (
       b'status', models.IntegerField(default=0, verbose_name=b'状态')),
      (
       b'created_at', models.DateTimeField(auto_now_add=True, verbose_name=b'时间')),
      (
       b'user_share_image', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=b'bee_django_referral.UserShareImage'))], options={b'db_table': b'bee_django_referral_record'}),
     migrations.AddField(model_name=b'activity', name=b'source_id', field=models.IntegerField(null=True, verbose_name=b'渠道id'))]