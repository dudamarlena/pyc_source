# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /webapp/bulbs/sections/migrations/0002_auto_20151103_1358.py
# Compiled at: 2016-09-22 15:00:17
# Size of source mod 2**32: 574 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('sections', '0001_initial')]
    operations = [
     migrations.AlterField(model_name='section', name='description', field=models.TextField(blank=True, default='')),
     migrations.AlterField(model_name='section', name='embed_code', field=models.TextField(blank=True, default=''))]