# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/trjg/code/venv/django-geo-db/lib/python3.5/site-packages/django_geo_db/migrations/0007_auto_20180310_0603.py
# Compiled at: 2018-03-10 20:33:06
# Size of source mod 2**32: 1893 bytes
from __future__ import unicode_literals
from django.db import migrations, models
import django.db.models.deletion, django_geo_db.models

class Migration(migrations.Migration):
    dependencies = [
     ('django_geo_db', '0006_auto_20180228_1147')]
    operations = [
     migrations.CreateModel(name='LocationBounds', fields=[
      (
       'location_bounds_id', models.AutoField(primary_key=True, serialize=False)),
      (
       'max_lat', models.DecimalField(decimal_places=6, max_digits=8)),
      (
       'min_lat', models.DecimalField(decimal_places=6, max_digits=8)),
      (
       'max_lon', models.DecimalField(decimal_places=6, max_digits=9)),
      (
       'min_lon', models.DecimalField(decimal_places=6, max_digits=9)),
      (
       'location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='django_geo_db.Location'))]),
     migrations.CreateModel(name='LocationMap', fields=[
      (
       'location_map_id', models.AutoField(primary_key=True, serialize=False)),
      (
       'file', models.FileField(upload_to='')),
      (
       'location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='django_geo_db.Location'))]),
     migrations.CreateModel(name='LocationMapType', fields=[
      (
       'location_map_type_id', models.AutoField(primary_key=True, serialize=False)),
      (
       'type', models.CharField(max_length=30))]),
     migrations.AddField(model_name='locationmap', name='type', field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='django_geo_db.LocationMapType'))]