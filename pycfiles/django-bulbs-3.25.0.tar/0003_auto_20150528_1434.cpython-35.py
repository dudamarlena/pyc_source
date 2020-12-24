# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /webapp/bulbs/campaigns/migrations/0003_auto_20150528_1434.py
# Compiled at: 2016-09-22 15:00:17
# Size of source mod 2**32: 457 bytes
from __future__ import unicode_literals
from django.db import models, migrations

class Migration(migrations.Migration):
    dependencies = [
     ('campaigns', '0002_auto_20150318_1926')]
    operations = [
     migrations.AlterField(model_name='campaignpixel', name='pixel_type', field=models.IntegerField(default=0, choices=[(0, b'Listing'), (1, b'Detail')]))]