# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /webapp/bulbs/special_coverage/migrations/0012_specialcoverage_super_features.py
# Compiled at: 2016-09-22 15:00:17
# Size of source mod 2**32: 523 bytes
from __future__ import unicode_literals
from django.db import migrations, models
import json_field.fields

class Migration(migrations.Migration):
    dependencies = [
     ('special_coverage', '0011_remove_specialcoverage_campaign')]
    operations = [
     migrations.AddField(model_name='specialcoverage', name='super_features', field=json_field.fields.JSONField(default=[], help_text='Enter a valid JSON object', blank=True))]