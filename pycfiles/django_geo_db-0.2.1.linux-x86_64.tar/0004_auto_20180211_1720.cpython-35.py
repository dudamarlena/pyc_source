# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/trjg/code/venv/django-geo-db/lib/python3.5/site-packages/django_geo_db/migrations/0004_auto_20180211_1720.py
# Compiled at: 2018-02-11 12:20:28
# Size of source mod 2**32: 431 bytes
from __future__ import unicode_literals
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
     ('django_geo_db', '0003_location_county')]
    operations = [
     migrations.AlterUniqueTogether(name='city', unique_together=set([('state', 'name', 'county')]))]