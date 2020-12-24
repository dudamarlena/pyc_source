# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /private/var/folders/6z/y737zg156f53v6d096dlmv500000gn/T/pip-build-YeCYrE/user-behavior/user_behavior/migrations/0001_initial.py
# Compiled at: 2016-11-17 22:38:22
from __future__ import unicode_literals
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion, jsonfield.fields

class Migration(migrations.Migration):
    initial = True
    dependencies = [
     ('contenttypes', '0002_remove_content_type_name'),
     migrations.swappable_dependency(settings.AUTH_USER_MODEL)]
    operations = [
     migrations.CreateModel(name=b'ApiInfo', fields=[
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
       b'user', models.ForeignKey(db_constraint=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name=b'user_behaviors', to=settings.AUTH_USER_MODEL))], options={b'db_table': b'api_info'}),
     migrations.CreateModel(name=b'UserBehavior', fields=[
      (
       b'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name=b'ID')),
      (
       b'created_at', models.DateTimeField(auto_now_add=True, null=True)),
      (
       b'updated_at', models.DateTimeField(auto_now=True, null=True)),
      (
       b'object_id', models.PositiveIntegerField(blank=True, null=True)),
      (
       b'api_info', models.ForeignKey(db_constraint=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name=b'user_behaviors', to=b'user_behavior.ApiInfo')),
      (
       b'content_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=b'contenttypes.ContentType'))], options={b'db_table': b'user_behavior'})]