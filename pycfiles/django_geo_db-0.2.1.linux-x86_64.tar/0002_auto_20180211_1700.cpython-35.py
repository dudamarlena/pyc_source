# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/trjg/code/venv/django-geo-db/lib/python3.5/site-packages/django_geo_db/migrations/0002_auto_20180211_1700.py
# Compiled at: 2018-02-11 12:00:11
# Size of source mod 2**32: 1517 bytes
from __future__ import unicode_literals
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('django_geo_db', '0001_initial')]
    operations = [
     migrations.CreateModel(name='County', fields=[
      (
       'county_id', models.AutoField(primary_key=True, serialize=False)),
      (
       'name', models.CharField(max_length=50)),
      (
       'generated_name', models.CharField(blank=True, max_length=50, null=True)),
      (
       'geocoordinate', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='django_geo_db.GeoCoordinate'))]),
     migrations.AlterField(model_name='state', name='name', field=models.CharField(max_length=50)),
     migrations.AddField(model_name='county', name='state', field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='django_geo_db.State')),
     migrations.AddField(model_name='city', name='county', field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='django_geo_db.County')),
     migrations.AlterUniqueTogether(name='county', unique_together=set([('state', 'name')]))]