# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/acs/devel/prosoul/django-prosoul/prosoul/migrations/0001_initial.py
# Compiled at: 2018-03-05 04:39:13
# Size of source mod 2**32: 7914 bytes
from __future__ import unicode_literals
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion, re

class Migration(migrations.Migration):
    initial = True
    dependencies = [
     migrations.swappable_dependency(settings.AUTH_USER_MODEL)]
    operations = [
     migrations.CreateModel(name='Attribute', fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'created_at', models.DateTimeField(auto_now_add=True)),
      (
       'updated_at', models.DateTimeField(auto_now=True)),
      (
       'active', models.BooleanField(default=True)),
      (
       'description', models.CharField(blank=True, default='', max_length=1024, null=True)),
      (
       'name', models.CharField(max_length=200, unique=True)),
      (
       'created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL))], options={'abstract': False}),
     migrations.CreateModel(name='DataSourceType', fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'created_at', models.DateTimeField(auto_now_add=True)),
      (
       'updated_at', models.DateTimeField(auto_now=True)),
      (
       'active', models.BooleanField(default=True)),
      (
       'description', models.CharField(blank=True, default='', max_length=1024, null=True)),
      (
       'name', models.CharField(max_length=200, unique=True)),
      (
       'created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL))], options={'abstract': False}),
     migrations.CreateModel(name='Factoid', fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'created_at', models.DateTimeField(auto_now_add=True)),
      (
       'updated_at', models.DateTimeField(auto_now=True)),
      (
       'active', models.BooleanField(default=True)),
      (
       'description', models.CharField(blank=True, default='', max_length=1024, null=True)),
      (
       'name', models.CharField(max_length=200, unique=True)),
      (
       'created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
      (
       'data_source_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='prosoul.DataSourceType'))], options={'abstract': False}),
     migrations.CreateModel(name='Goal', fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'created_at', models.DateTimeField(auto_now_add=True)),
      (
       'updated_at', models.DateTimeField(auto_now=True)),
      (
       'active', models.BooleanField(default=True)),
      (
       'description', models.CharField(blank=True, default='', max_length=1024, null=True)),
      (
       'name', models.CharField(max_length=200, unique=True)),
      (
       'attributes', models.ManyToManyField(to='prosoul.Attribute')),
      (
       'created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
      (
       'subgoals', models.ManyToManyField(blank=True, to='prosoul.Goal'))], options={'abstract': False}),
     migrations.CreateModel(name='Metric', fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'created_at', models.DateTimeField(auto_now_add=True)),
      (
       'updated_at', models.DateTimeField(auto_now=True)),
      (
       'active', models.BooleanField(default=True)),
      (
       'description', models.CharField(blank=True, default='', max_length=1024, null=True)),
      (
       'name', models.CharField(max_length=200, unique=True)),
      (
       'thresholds', models.CharField(blank=True, default=None, max_length=200, null=True, validators=[django.core.validators.RegexValidator(re.compile('^\\d+(?:\\,\\d+)*\\Z', 32), code='invalid', message='Enter only digits separated by commas.')])),
      (
       'created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL))], options={'abstract': False}),
     migrations.CreateModel(name='MetricData', fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'created_at', models.DateTimeField(auto_now_add=True)),
      (
       'updated_at', models.DateTimeField(auto_now=True)),
      (
       'active', models.BooleanField(default=True)),
      (
       'description', models.CharField(blank=True, default='', max_length=1024, null=True)),
      (
       'implementation', models.CharField(blank=True, max_length=200, null=True)),
      (
       'created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL))], options={'abstract': False}),
     migrations.CreateModel(name='QualityModel', fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'created_at', models.DateTimeField(auto_now_add=True)),
      (
       'updated_at', models.DateTimeField(auto_now=True)),
      (
       'active', models.BooleanField(default=True)),
      (
       'description', models.CharField(blank=True, default='', max_length=1024, null=True)),
      (
       'name', models.CharField(max_length=200, unique=True)),
      (
       'created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
      (
       'goals', models.ManyToManyField(to='prosoul.Goal'))], options={'abstract': False}),
     migrations.AddField(model_name='metric', name='data', field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='prosoul.MetricData')),
     migrations.AddField(model_name='metric', name='data_source_type', field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='prosoul.DataSourceType')),
     migrations.AddField(model_name='attribute', name='factoids', field=models.ManyToManyField(blank=True, to='prosoul.Factoid')),
     migrations.AddField(model_name='attribute', name='metrics', field=models.ManyToManyField(blank=True, to='prosoul.Metric')),
     migrations.AddField(model_name='attribute', name='subattributes', field=models.ManyToManyField(blank=True, to='prosoul.Attribute'))]