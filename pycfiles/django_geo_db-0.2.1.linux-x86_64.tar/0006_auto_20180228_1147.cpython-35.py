# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/trjg/code/venv/django-geo-db/lib/python3.5/site-packages/django_geo_db/migrations/0006_auto_20180228_1147.py
# Compiled at: 2018-02-28 07:19:16
# Size of source mod 2**32: 1080 bytes
from __future__ import unicode_literals
from django.db import migrations, models
import django_geo_db.models

class Migration(migrations.Migration):
    dependencies = [
     ('django_geo_db', '0005_geographicregion')]
    operations = [
     migrations.AddField(model_name='geocoordinate', name='lat_ten_thousands', field=django_geo_db.models.IntegerRangeField(blank=True, null=True)),
     migrations.AddField(model_name='geocoordinate', name='lon_ten_thousands', field=django_geo_db.models.IntegerRangeField(blank=True, null=True)),
     migrations.AlterField(model_name='geocoordinate', name='lat', field=models.DecimalField(decimal_places=6, max_digits=8)),
     migrations.AlterField(model_name='geocoordinate', name='lon', field=models.DecimalField(decimal_places=6, max_digits=9))]