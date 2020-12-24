# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/arroyo/projects/cpmd/server/api/django-google-address/google_address/migrations/0002_auto_20170417_2307.py
# Compiled at: 2017-04-17 19:07:05
# Size of source mod 2**32: 2390 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    initial = True
    dependencies = [
     ('google_address', '0001_initial')]
    operations = [
     migrations.CreateModel(name='AddressComponent', fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'long_name', models.CharField(max_length=400)),
      (
       'short_name', models.CharField(max_length=400))]),
     migrations.CreateModel(name='AddressComponentType', fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'name', models.CharField(max_length=100))]),
     migrations.CreateModel(name='GoogleAddress', fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'typed_address', models.CharField(blank=True, max_length=400, null=True)),
      (
       'typed_address2', models.CharField(blank=True, max_length=400, null=True)),
      (
       'address_line', models.CharField(blank=True, max_length=400, null=True)),
      (
       'city_state', models.CharField(blank=True, max_length=400, null=True)),
      (
       'lat', models.FloatField(blank=True, null=True, verbose_name='lat')),
      (
       'lng', models.FloatField(blank=True, null=True, verbose_name='lng')),
      (
       'address_components', models.ManyToManyField(to='google_address.AddressComponent'))]),
     migrations.CreateModel(name='GoogleRegion', fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'region_name', models.CharField(max_length=400)),
      (
       'filter_by', models.CharField(max_length=400))]),
     migrations.AddField(model_name='addresscomponent', name='types', field=models.ManyToManyField(to='google_address.AddressComponentType'))]