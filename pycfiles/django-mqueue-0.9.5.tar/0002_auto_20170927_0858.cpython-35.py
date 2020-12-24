# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ggg/www/dev/mogos/mogo78/mogo/mqueue/migrations/0002_auto_20170927_0858.py
# Compiled at: 2017-09-27 04:58:20
# Size of source mod 2**32: 455 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('mqueue', '0001_initial')]
    operations = [
     migrations.AlterField(model_name='mevent', name='data', field=models.TextField(blank=True, verbose_name='Data'))]