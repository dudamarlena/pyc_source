# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/huangwei/code/bee_apps_site/bee_django_social_feed/migrations/0015_auto_20181018_0834.py
# Compiled at: 2018-10-17 20:34:51
from __future__ import unicode_literals
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     migrations.swappable_dependency(settings.AUTH_USER_MODEL),
     ('bee_django_social_feed', '0014_auto_20180929_1051')]
    operations = [
     migrations.CreateModel(name=b'FeedStickSettings', fields=[
      (
       b'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name=b'ID')),
      (
       b'number', models.IntegerField(default=1, verbose_name=b'置顶条数')),
      (
       b'duration', models.IntegerField(default=1, verbose_name=b'置顶天数')),
      (
       b'user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL))]),
     migrations.AddField(model_name=b'feed', name=b'is_stick', field=models.BooleanField(default=False, verbose_name=b'是否置顶')),
     migrations.AddField(model_name=b'feed', name=b'stick_expired_at', field=models.DateTimeField(blank=True, null=True, verbose_name=b'置顶失效日期'))]