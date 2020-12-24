# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /webapp/bulbs/special_coverage/migrations/0005_auto_20151103_1358.py
# Compiled at: 2016-09-22 15:00:17
# Size of source mod 2**32: 438 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('special_coverage', '0004_specialcoverage_config')]
    operations = [
     migrations.AlterField(model_name='specialcoverage', name='description', field=models.TextField(blank=True, default=''))]