# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/build/smn/heatherr/heatherr/migrations/0001_initial.py
# Compiled at: 2016-01-28 05:47:10
from __future__ import unicode_literals
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    initial = True
    dependencies = [
     migrations.swappable_dependency(settings.AUTH_USER_MODEL)]
    operations = [
     migrations.CreateModel(name=b'SlackAccount', fields=[
      (
       b'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name=b'ID')),
      (
       b'access_token', models.CharField(max_length=255)),
      (
       b'scope', models.CharField(max_length=255)),
      (
       b'team_name', models.CharField(max_length=255)),
      (
       b'team_id', models.CharField(max_length=255)),
      (
       b'incoming_webhook_url', models.CharField(max_length=255)),
      (
       b'incoming_webhook_channel', models.CharField(max_length=255)),
      (
       b'incoming_webhook_configuration_url', models.CharField(max_length=255)),
      (
       b'bot_user_id', models.CharField(max_length=255)),
      (
       b'bot_access_token', models.CharField(max_length=255)),
      (
       b'created_at', models.DateTimeField(auto_now_add=True)),
      (
       b'updated_at', models.DateTimeField(auto_now=True)),
      (
       b'user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL))])]