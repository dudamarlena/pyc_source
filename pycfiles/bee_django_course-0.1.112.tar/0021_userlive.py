# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_course/migrations/0021_userlive.py
# Compiled at: 2018-04-01 07:23:14
from __future__ import unicode_literals
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     migrations.swappable_dependency(settings.AUTH_USER_MODEL),
     ('bee_django_course', '0020_auto_20180326_1358')]
    operations = [
     migrations.CreateModel(name=b'UserLive', fields=[
      (
       b'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name=b'ID')),
      (
       b'provider_name', models.CharField(max_length=180)),
      (
       b'cc_user_id', models.CharField(max_length=180, null=True)),
      (
       b'room_id', models.CharField(max_length=180, null=True)),
      (
       b'live_id', models.CharField(max_length=180, null=True)),
      (
       b'stop_status', models.CharField(max_length=180, null=True)),
      (
       b'record_status', models.CharField(max_length=180, null=True)),
      (
       b'record_video_id', models.CharField(max_length=180, null=True)),
      (
       b'replay_url', models.CharField(max_length=180, null=True)),
      (
       b'start_time', models.DateTimeField(null=True)),
      (
       b'end_time', models.DateTimeField(null=True)),
      (
       b'duration', models.IntegerField(null=True)),
      (
       b'record_video_duration', models.IntegerField(null=True)),
      (
       b'status', models.IntegerField(default=1, null=True)),
      (
       b'created_at', models.DateTimeField(auto_now_add=True)),
      (
       b'call_count', models.IntegerField(default=0)),
      (
       b'user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL))], options={b'ordering': [
                    b'-created_at'], 
        b'db_table': b'user_live'})]