# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /webapp/bulbs/videos/migrations/0002_auto_20160613_1116.py
# Compiled at: 2016-09-22 15:00:17
# Size of source mod 2**32: 451 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('videos', '0001_initial')]
    operations = [
     migrations.AlterField(model_name='videohubvideo', name='id', field=models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True))]