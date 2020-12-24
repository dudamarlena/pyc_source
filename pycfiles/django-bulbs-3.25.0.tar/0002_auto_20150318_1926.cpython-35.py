# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /webapp/bulbs/campaigns/migrations/0002_auto_20150318_1926.py
# Compiled at: 2016-09-22 15:00:17
# Size of source mod 2**32: 396 bytes
from __future__ import unicode_literals
from django.db import models, migrations

class Migration(migrations.Migration):
    dependencies = [
     ('campaigns', '0001_initial')]
    operations = [
     migrations.RenameField(model_name='campaignpixel', old_name='campaign_type', new_name='pixel_type')]