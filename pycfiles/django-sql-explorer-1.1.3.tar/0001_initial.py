# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/muhammadelias/grove_core/django-sql-explorer/explorer/migrations/0001_initial.py
# Compiled at: 2019-07-02 16:47:10
from __future__ import unicode_literals
from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings

class Migration(migrations.Migration):
    dependencies = [
     migrations.swappable_dependency(settings.AUTH_USER_MODEL)]
    operations = [
     migrations.CreateModel(name=b'Query', fields=[
      (
       b'id', models.AutoField(verbose_name=b'ID', serialize=False, auto_created=True, primary_key=True)),
      (
       b'title', models.CharField(max_length=255)),
      (
       b'sql', models.TextField()),
      (
       b'description', models.TextField(null=True, blank=True)),
      (
       b'created_at', models.DateTimeField(auto_now_add=True)),
      (
       b'last_run_date', models.DateTimeField(auto_now=True)),
      (
       b'created_by_user', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE))], options={b'ordering': [
                    b'title'], 
        b'verbose_name_plural': b'Queries'}, bases=(
      models.Model,)),
     migrations.CreateModel(name=b'QueryLog', fields=[
      (
       b'id', models.AutoField(verbose_name=b'ID', serialize=False, auto_created=True, primary_key=True)),
      (
       b'sql', models.TextField()),
      (
       b'is_playground', models.BooleanField(default=False)),
      (
       b'run_at', models.DateTimeField(auto_now_add=True)),
      (
       b'query', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to=b'explorer.Query', null=True)),
      (
       b'run_by_user', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE))], options={b'ordering': [
                    b'-run_at']}, bases=(
      models.Model,))]