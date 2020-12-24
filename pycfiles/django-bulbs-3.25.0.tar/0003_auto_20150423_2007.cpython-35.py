# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /webapp/bulbs/special_coverage/migrations/0003_auto_20150423_2007.py
# Compiled at: 2016-09-22 15:00:17
# Size of source mod 2**32: 584 bytes
from __future__ import unicode_literals
from django.db import models, migrations
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('special_coverage', '0002_auto_20150318_2110')]
    operations = [
     migrations.AlterField(model_name='specialcoverage', name='campaign', field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, default=None, blank=True, to='campaigns.Campaign', null=True), preserve_default=True)]