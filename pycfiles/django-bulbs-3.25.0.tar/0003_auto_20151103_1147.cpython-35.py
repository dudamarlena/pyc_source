# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /webapp/bulbs/contributions/migrations/0003_auto_20151103_1147.py
# Compiled at: 2016-09-22 15:00:17
# Size of source mod 2**32: 425 bytes
from __future__ import unicode_literals
from django.db import models, migrations

class Migration(migrations.Migration):
    dependencies = [
     ('contributions', '0002_auto_20151001_1201')]
    operations = [
     migrations.AlterField(model_name='freelanceprofile', name='is_manager', field=models.BooleanField(default=False))]