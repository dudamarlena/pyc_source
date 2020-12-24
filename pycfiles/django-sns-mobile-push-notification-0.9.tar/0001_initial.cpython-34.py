# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/rvaziri/django_mobile_push/sns_mobile_push_notification/migrations/0001_initial.py
# Compiled at: 2018-04-29 13:22:49
# Size of source mod 2**32: 1860 bytes
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
     migrations.CreateModel(name='Device', fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'created_at', models.DateTimeField(auto_now_add=True)),
      (
       'updated_at', models.DateTimeField(auto_now=True)),
      (
       'os', models.IntegerField(choices=[(0, 'IOS'), (1, 'Android')])),
      (
       'token', models.CharField(max_length=255, unique=True)),
      (
       'arn', models.CharField(blank=True, max_length=255, null=True, unique=True)),
      (
       'active', models.BooleanField(default=True))], options={'ordering': [
                   '-id']}),
     migrations.CreateModel(name='Log', fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'created_at', models.DateTimeField(auto_now_add=True)),
      (
       'updated_at', models.DateTimeField(auto_now=True)),
      (
       'notification_type', models.CharField(blank=True, max_length=255, null=True)),
      (
       'arn', models.CharField(blank=True, max_length=255, null=True)),
      (
       'message', models.TextField(blank=True, null=True)),
      (
       'response', models.TextField(blank=True, null=True)),
      (
       'device', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='notification_logs', to='sns_mobile_push_notification.Device'))])]