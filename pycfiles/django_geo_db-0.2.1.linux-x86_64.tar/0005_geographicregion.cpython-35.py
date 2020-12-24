# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/trjg/code/venv/django-geo-db/lib/python3.5/site-packages/django_geo_db/migrations/0005_geographicregion.py
# Compiled at: 2018-02-17 18:50:12
# Size of source mod 2**32: 656 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('django_geo_db', '0004_auto_20180211_1720')]
    operations = [
     migrations.CreateModel(name='GeographicRegion', fields=[
      (
       'geographic_region_id', models.AutoField(primary_key=True, serialize=False)),
      (
       'name', models.CharField(max_length=40)),
      (
       'locations', models.ManyToManyField(to='django_geo_db.Location'))])]