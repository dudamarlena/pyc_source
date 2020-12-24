# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/tonra/ohm2/clients/ohm2/entwicklung/ohm2-dev-light/webapp/backend/apps/ohm2_addresses_light/migrations/0002_auto_20170913_2121.py
# Compiled at: 2017-09-13 17:21:44
# Size of source mod 2**32: 680 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('ohm2_addresses_light', '0001_initial')]
    operations = [
     migrations.AlterField(model_name='address', name='number', field=models.CharField(blank=True, default='', max_length=512, null=True)),
     migrations.AlterField(model_name='address', name='street', field=models.CharField(blank=True, default='', max_length=512, null=True))]