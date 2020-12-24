# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/tonra/ohm2/clients/ohm2/entwicklung/ohm2-dev-light/webapp/backend/apps/ohm2_addresses_light/migrations/0001_initial.py
# Compiled at: 2017-09-01 16:03:42
# Size of source mod 2**32: 2052 bytes
from __future__ import unicode_literals
import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.db.models.deletion, django.utils.timezone

class Migration(migrations.Migration):
    initial = True
    dependencies = [
     ('ohm2_countries_light', '0001_initial')]
    operations = [
     migrations.CreateModel(name='Address', fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'identity', models.CharField(max_length=2048, unique=True)),
      (
       'created', models.DateTimeField(default=django.utils.timezone.now)),
      (
       'last_update', models.DateTimeField(default=django.utils.timezone.now)),
      (
       'first_level', models.CharField(blank=True, default='', max_length=512, null=True)),
      (
       'second_level', models.CharField(blank=True, default='', max_length=512, null=True)),
      (
       'third_level', models.CharField(blank=True, default='', max_length=512, null=True)),
      (
       'fourth_level', models.CharField(blank=True, default='', max_length=512, null=True)),
      (
       'street', models.CharField(max_length=512)),
      (
       'number', models.CharField(max_length=512)),
      (
       'floor', models.CharField(blank=True, default='', max_length=512, null=True)),
      (
       'tower', models.CharField(blank=True, default='', max_length=512, null=True)),
      (
       'block', models.CharField(blank=True, default='', max_length=512, null=True)),
      (
       'coordinates', django.contrib.gis.db.models.fields.PointField(blank=True, default=None, null=True, srid=4326)),
      (
       'country', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ohm2_countries_light.Country'))], options={'abstract': False})]