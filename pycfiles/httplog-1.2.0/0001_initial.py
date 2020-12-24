# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: d:\users\ma_k\appdata\local\temp\pip-build-s8wja0\httplog\httplog\migrations\0001_initial.py
# Compiled at: 2016-11-28 21:21:16
from __future__ import unicode_literals
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion, jsonfield.fields

class Migration(migrations.Migration):
    initial = True
    dependencies = [
     migrations.swappable_dependency(settings.AUTH_USER_MODEL)]
    operations = [
     migrations.CreateModel(name=b'HttpLog', fields=[
      (
       b'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name=b'ID')),
      (
       b'created_at', models.DateTimeField(auto_now_add=True, null=True)),
      (
       b'updated_at', models.DateTimeField(auto_now=True, null=True)),
      (
       b'client', jsonfield.fields.JSONField(blank=True, default={}, null=True)),
      (
       b'server', jsonfield.fields.JSONField(blank=True, default={}, null=True)),
      (
       b'request', jsonfield.fields.JSONField(blank=True, default={}, null=True)),
      (
       b'response', jsonfield.fields.JSONField(blank=True, default={}, null=True)),
      (
       b'name', models.CharField(blank=True, max_length=256, null=True)),
      (
       b'user', models.ForeignKey(db_constraint=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name=b'httplogs', to=settings.AUTH_USER_MODEL))], options={b'db_table': b'httplog'})]