# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/f1nal/Dropbox/python/jet-bridge/src/packages/jet_django/jet_django/migrations/0001_initial.py
# Compiled at: 2019-10-30 05:24:12
# Size of source mod 2**32: 5152 bytes
from __future__ import unicode_literals
from django.db import migrations, models
import django.db.models.deletion, django.utils.timezone

class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
     migrations.CreateModel(name='Dashboard', fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'name', models.CharField(max_length=255, verbose_name='name')),
      (
       'ordering', models.PositiveIntegerField(default=0, verbose_name='ordering')),
      (
       'date_add', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date added'))], options={'verbose_name': 'dashboard', 
      'verbose_name_plural': 'dashboards', 
      'ordering': ('ordering', )}),
     migrations.CreateModel(name='MenuSettings', fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'items', models.TextField(blank=True, default='', verbose_name='items')),
      (
       'date_add', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date added'))], options={'verbose_name': 'menu settings', 
      'verbose_name_plural': 'menu settings'}),
     migrations.CreateModel(name='ModelDescription', fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'app_label', models.CharField(max_length=255, verbose_name='app_label')),
      (
       'model', models.CharField(blank=True, default='', max_length=255, verbose_name='model')),
      (
       'params', models.TextField(blank=True, default='', verbose_name='params')),
      (
       'date_add', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date added'))], options={'verbose_name': 'model description', 
      'verbose_name_plural': 'model descriptions'}),
     migrations.CreateModel(name='Token', fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'project', models.CharField(blank=True, default='', max_length=30, verbose_name='project')),
      (
       'token', models.UUIDField(verbose_name='token')),
      (
       'date_add', models.DateTimeField(verbose_name='date added'))], options={'verbose_name': 'token', 
      'verbose_name_plural': 'tokens'}),
     migrations.CreateModel(name='ViewSettings', fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'app_label', models.CharField(max_length=255, verbose_name='app_label')),
      (
       'model', models.CharField(blank=True, default='', max_length=255, verbose_name='model')),
      (
       'view', models.CharField(blank=True, default='change', max_length=255, verbose_name='view')),
      (
       'params', models.TextField(blank=True, default='', verbose_name='params')),
      (
       'date_add', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date added'))], options={'verbose_name': 'view settings', 
      'verbose_name_plural': 'views settings'}),
     migrations.CreateModel(name='Widget', fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'widget_type', models.CharField(max_length=255, verbose_name='type')),
      (
       'name', models.CharField(max_length=255, verbose_name='name')),
      (
       'x', models.PositiveSmallIntegerField(verbose_name='x')),
      (
       'y', models.PositiveSmallIntegerField(verbose_name='y')),
      (
       'width', models.PositiveSmallIntegerField(default=1, verbose_name='width')),
      (
       'height', models.PositiveSmallIntegerField(default=1, verbose_name='height')),
      (
       'params', models.TextField(blank=True, default='', verbose_name='params')),
      (
       'date_add', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date added')),
      (
       'dashboard', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='widgets', to='jet_django.Dashboard', verbose_name='dashboard'))], options={'verbose_name': 'widget', 
      'verbose_name_plural': 'widgets', 
      'ordering': ('y', 'x')})]