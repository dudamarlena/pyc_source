# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/gkarak/workspace/python/team_reset/ninecms/migrations/0002_auto_20150519_1102.py
# Compiled at: 2015-05-19 04:03:04
# Size of source mod 2**32: 575 bytes
from __future__ import unicode_literals
from django.db import models, migrations

class Migration(migrations.Migration):
    dependencies = [
     ('ninecms', '0001_squashed_0024_auto_20150416_1551')]
    operations = [
     migrations.AlterField(model_name='menuitem', name='title', field=models.CharField(max_length=255)),
     migrations.AlterField(model_name='taxonomyterm', name='name', field=models.CharField(max_length=50))]