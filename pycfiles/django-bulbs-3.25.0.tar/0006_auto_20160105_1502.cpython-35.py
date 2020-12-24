# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /webapp/bulbs/contributions/migrations/0006_auto_20160105_1502.py
# Compiled at: 2016-09-22 15:00:17
# Size of source mod 2**32: 407 bytes
from __future__ import unicode_literals
from django.db import models, migrations

class Migration(migrations.Migration):
    dependencies = [
     ('contributions', '0005_auto_20151130_1036')]
    operations = [
     migrations.AlterField(model_name='lineitem', name='amount', field=models.FloatField(default=0))]