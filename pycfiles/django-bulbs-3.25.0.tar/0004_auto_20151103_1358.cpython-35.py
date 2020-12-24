# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /webapp/bulbs/contributions/migrations/0004_auto_20151103_1358.py
# Compiled at: 2016-09-22 15:00:17
# Size of source mod 2**32: 743 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('contributions', '0003_auto_20151103_1147')]
    operations = [
     migrations.AlterField(model_name='contributorrole', name='payment_type', field=models.IntegerField(choices=[(0, 'Flat Rate'), (1, 'FeatureType'), (2, 'Hourly'), (3, 'Manual')], default=3)),
     migrations.AlterField(model_name='rate', name='name', field=models.IntegerField(null=True, choices=[(0, 'Flat Rate'), (1, 'FeatureType'), (2, 'Hourly'), (3, 'Manual'), (4, 'Override')]))]