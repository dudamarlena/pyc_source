# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/arroyo/ovp/suzano-ovp/django-ovp-projects/ovp_projects/migrations/0002_auto_20161019_1557.py
# Compiled at: 2017-02-22 17:56:49
# Size of source mod 2**32: 2207 bytes
from __future__ import unicode_literals
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    initial = True
    dependencies = [
     migrations.swappable_dependency(settings.AUTH_USER_MODEL),
     ('ovp_projects', '0001_initial')]
    operations = [
     migrations.CreateModel(name='Project', fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'name', models.CharField(max_length=100, verbose_name='Project name')),
      (
       'slug', models.SlugField(max_length=100, unique=True)),
      (
       'published', models.BooleanField(default=False, verbose_name='Published')),
      (
       'highlighted', models.BooleanField(default=False, verbose_name='Highlighted')),
      (
       'published_date', models.DateTimeField(blank=True, null=True, verbose_name='Published date')),
      (
       'closed', models.BooleanField(default=False, verbose_name='Closed')),
      (
       'closed_date', models.DateTimeField(blank=True, null=True, verbose_name='Closed date')),
      (
       'deleted', models.BooleanField(default=False, verbose_name='Deleted')),
      (
       'deleted_date', models.DateTimeField(blank=True, null=True, verbose_name='Deleted date')),
      (
       'created_date', models.DateTimeField(auto_now_add=True)),
      (
       'modified_date', models.DateTimeField(auto_now=True)),
      (
       'owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL))]),
     migrations.CreateModel(name='Role', fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'))]),
     migrations.AddField(model_name='project', name='roles', field=models.ManyToManyField(blank=True, to='ovp_projects.Role', verbose_name='Roles'))]