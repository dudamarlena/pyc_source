# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/juliocesar/work/me/django-world-regions/django-world-regions/world_regions/migrations/0001_initial.py
# Compiled at: 2015-07-05 06:12:13
from __future__ import unicode_literals
from django.core.management import call_command
from django.db import models, migrations
import django_countries.fields

def load_data_in_fixtures(apps, schema_editor):
    call_command(b'loaddata', b'initial_data', app_label=b'world_regions')


class Migration(migrations.Migration):
    dependencies = []
    operations = [
     migrations.CreateModel(name=b'Region', fields=[
      (
       b'id', models.AutoField(verbose_name=b'ID', serialize=False, auto_created=True, primary_key=True)),
      (
       b'name', models.CharField(max_length=25)),
      (
       b'code', models.CharField(max_length=3))]),
     migrations.CreateModel(name=b'RegionCountry', fields=[
      (
       b'id', models.AutoField(verbose_name=b'ID', serialize=False, auto_created=True, primary_key=True)),
      (
       b'country', django_countries.fields.CountryField(unique=True, max_length=2)),
      (
       b'region', models.ForeignKey(related_name=b'countries', to=b'world_regions.Region'))]),
     migrations.RunPython(load_data_in_fixtures)]