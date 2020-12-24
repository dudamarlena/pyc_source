# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/notifications/migrations/0001_initial.py
# Compiled at: 2019-02-21 19:38:07
# Size of source mod 2**32: 1475 bytes
from __future__ import unicode_literals
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    initial = True
    dependencies = [
     migrations.swappable_dependency(settings.AUTH_USER_MODEL)]
    operations = [
     migrations.CreateModel(name='Notification',
       fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'source_display_name', models.CharField(max_length=150)),
      (
       'action', models.CharField(max_length=50)),
      (
       'category', models.CharField(max_length=50)),
      (
       'obj', models.IntegerField()),
      (
       'url', models.URLField()),
      (
       'is_read', models.BooleanField(default=False)),
      (
       'create_date', models.DateTimeField(auto_now_add=True)),
      (
       'update_date', models.DateTimeField(auto_now=True)),
      (
       'short_description', models.CharField(max_length=100)),
      (
       'recipent', models.ForeignKey(on_delete=(django.db.models.deletion.CASCADE), related_name='notifications', to=(settings.AUTH_USER_MODEL))),
      (
       'source', models.ForeignKey(on_delete=(django.db.models.deletion.CASCADE), to=(settings.AUTH_USER_MODEL)))])]