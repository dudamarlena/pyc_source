# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /webapp/bulbs/special_coverage/migrations/0007_auto_20160111_1114.py
# Compiled at: 2016-09-22 15:00:17
# Size of source mod 2**32: 608 bytes
from __future__ import unicode_literals
from django.db import models, migrations

class Migration(migrations.Migration):
    dependencies = [
     ('special_coverage', '0006_auto_20151109_1708')]
    operations = [
     migrations.AddField(model_name='specialcoverage', name='end_date', field=models.DateTimeField(null=True, blank=True)),
     migrations.AddField(model_name='specialcoverage', name='start_date', field=models.DateTimeField(null=True, blank=True))]