# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dmeliza/Devel/django-neurobank/neurobank/migrations/0001_initial.py
# Compiled at: 2018-02-07 19:02:58
# Size of source mod 2**32: 3277 bytes
from __future__ import unicode_literals
from django.contrib.postgres.operations import HStoreExtension
from django.conf import settings
import django.contrib.postgres.fields.hstore
from django.db import migrations, models
import django.db.models.deletion, neurobank.tools

class Migration(migrations.Migration):
    initial = True
    dependencies = [
     migrations.swappable_dependency(settings.AUTH_USER_MODEL)]
    operations = [
     HStoreExtension(),
     migrations.CreateModel(name='DataType',
       fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'name', models.SlugField(max_length=32, unique=True)),
      (
       'content_type', models.CharField(blank=True, max_length=128, null=True))]),
     migrations.CreateModel(name='Domain',
       fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'name', models.SlugField(help_text='a descriptive name', max_length=32, unique=True)),
      (
       'scheme', models.CharField(max_length=16)),
      (
       'root', models.CharField(help_text='root path for resources', max_length=512))]),
     migrations.CreateModel(name='Location',
       fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'domain', models.ForeignKey(on_delete=(django.db.models.deletion.CASCADE), to='neurobank.Domain'))]),
     migrations.CreateModel(name='Resource',
       fields=[
      (
       'id', models.AutoField(primary_key=True, serialize=False)),
      (
       'name', models.SlugField(default=(neurobank.tools.random_id), max_length=64, unique=True)),
      (
       'sha1', models.CharField(blank=True, help_text='specify only for resources whose contents must not change (i.e., sources)', max_length=40, null=True, unique=True)),
      (
       'created_on', models.DateTimeField(auto_now_add=True)),
      (
       'metadata', django.contrib.postgres.fields.hstore.HStoreField(blank=True, null=True)),
      (
       'created_by', models.ForeignKey(on_delete=(django.db.models.deletion.CASCADE), related_name='resources', to=(settings.AUTH_USER_MODEL))),
      (
       'dtype', models.ForeignKey(on_delete=(django.db.models.deletion.PROTECT), to='neurobank.DataType')),
      (
       'locations', models.ManyToManyField(through='neurobank.Location', to='neurobank.Domain'))]),
     migrations.AddField(model_name='location',
       name='resource',
       field=models.ForeignKey(on_delete=(django.db.models.deletion.CASCADE), to='neurobank.Resource')),
     migrations.AlterUniqueTogether(name='domain',
       unique_together=(set([('scheme', 'root')]))),
     migrations.AlterUniqueTogether(name='location',
       unique_together=(set([('resource', 'domain')])))]