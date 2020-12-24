# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/huangwei/code/bee_apps_site/bee_django_social_feed/migrations/0004_feedimage.py
# Compiled at: 2018-06-25 23:11:06
from __future__ import unicode_literals
from django.db import migrations, models
import django.db.models.deletion, django.utils.timezone

class Migration(migrations.Migration):
    dependencies = [
     ('bee_django_social_feed', '0003_auto_20180617_1053')]
    operations = [
     migrations.CreateModel(name=b'FeedImage', fields=[
      (
       b'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name=b'ID')),
      (
       b'image', models.ImageField(upload_to=b'feeds/%Y/%m/%d', verbose_name=b'图片')),
      (
       b'created_at', models.DateTimeField(default=django.utils.timezone.now)),
      (
       b'feed', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=b'bee_django_social_feed.Feed', verbose_name=b'日志'))])]