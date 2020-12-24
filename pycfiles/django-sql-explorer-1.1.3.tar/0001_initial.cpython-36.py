# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/muhammadelias/grove_core/django-sql-explorer/explorer/migrations/0001_initial.py
# Compiled at: 2019-07-02 16:47:10
# Size of source mod 2**32: 1961 bytes
from __future__ import unicode_literals
from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings

class Migration(migrations.Migration):
    dependencies = [
     migrations.swappable_dependency(settings.AUTH_USER_MODEL)]
    operations = [
     migrations.CreateModel(name='Query',
       fields=[
      (
       'id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
      (
       'title', models.CharField(max_length=255)),
      (
       'sql', models.TextField()),
      (
       'description', models.TextField(null=True, blank=True)),
      (
       'created_at', models.DateTimeField(auto_now_add=True)),
      (
       'last_run_date', models.DateTimeField(auto_now=True)),
      (
       'created_by_user', models.ForeignKey(blank=True, to=(settings.AUTH_USER_MODEL), null=True, on_delete=(models.CASCADE)))],
       options={'ordering':[
       'title'], 
      'verbose_name_plural':'Queries'},
       bases=(
      models.Model,)),
     migrations.CreateModel(name='QueryLog',
       fields=[
      (
       'id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
      (
       'sql', models.TextField()),
      (
       'is_playground', models.BooleanField(default=False)),
      (
       'run_at', models.DateTimeField(auto_now_add=True)),
      (
       'query', models.ForeignKey(on_delete=(django.db.models.deletion.SET_NULL), blank=True, to='explorer.Query', null=True)),
      (
       'run_by_user', models.ForeignKey(blank=True, to=(settings.AUTH_USER_MODEL), null=True, on_delete=(models.CASCADE)))],
       options={'ordering': ['-run_at']},
       bases=(
      models.Model,))]