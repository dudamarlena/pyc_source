# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/trjg/code/venv/django-geo-db/lib/python3.5/site-packages/django_geo_db/migrations/0003_location_county.py
# Compiled at: 2018-02-11 12:10:25
# Size of source mod 2**32: 569 bytes
from __future__ import unicode_literals
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('django_geo_db', '0002_auto_20180211_1700')]
    operations = [
     migrations.AddField(model_name='location', name='county', field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='django_geo_db.County'))]