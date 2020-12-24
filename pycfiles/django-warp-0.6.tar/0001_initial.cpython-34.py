# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/enrico/Dropbox/dev/django-warp/django_warp/migrations/0001_initial.py
# Compiled at: 2016-05-25 16:04:11
# Size of source mod 2**32: 2425 bytes
from __future__ import unicode_literals
from django.db import migrations, models
import django.db.models.deletion, django_warp.models

class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
     migrations.CreateModel(name='datasets', fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'name', models.CharField(max_length=50)),
      (
       'slug', models.CharField(blank=True, max_length=50)),
      (
       'epsg', models.IntegerField(default='3857')),
      (
       'extentLeft', models.FloatField(default='-20000000.00')),
      (
       'extentBottom', models.FloatField(default='-10000000.00')),
      (
       'extentRight', models.FloatField(default='20000000.00')),
      (
       'extentTop', models.FloatField(default='20000000.00')),
      (
       'baselayer', models.TextField(blank=True, default='new ol.layer.Tile({\n    source: new ol.source.OSM()\n}),'))]),
     migrations.CreateModel(name='rasterMaps', fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'titolo', models.CharField(max_length=50)),
      (
       'slug', models.CharField(blank=True, max_length=50)),
      (
       'note', models.TextField(blank=True)),
      (
       'sorgente', models.ImageField(upload_to='warp/', validators=[django_warp.models.validate_file_extension])),
      (
       'destinazione', models.ImageField(blank=True, upload_to='warp/')),
      (
       'webimg', models.ImageField(blank=True, upload_to='warp/')),
      (
       'correlazione', models.TextField(blank=True)),
      (
       'clipSorgente', models.TextField(blank=True)),
      (
       'clipDestinazione', models.TextField(blank=True)),
      (
       'dataset', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='current_dataset', to='django_warp.datasets')),
      (
       'datasetRecover', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='recover_dataset', to='django_warp.datasets'))])]