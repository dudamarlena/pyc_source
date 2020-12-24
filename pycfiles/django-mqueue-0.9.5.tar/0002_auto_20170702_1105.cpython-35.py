# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ggg/www/dev/mogos/mogo54/mogo/mqueue/migrations/0002_auto_20170702_1105.py
# Compiled at: 2017-07-02 07:05:56
# Size of source mod 2**32: 673 bytes
from __future__ import unicode_literals
from django.db import migrations, models
import jsonfield.fields

class Migration(migrations.Migration):
    dependencies = [
     ('mqueue', '0001_initial')]
    operations = [
     migrations.AddField(model_name='mevent', name='bucket', field=models.CharField(blank=True, max_length=60, verbose_name='Bucket')),
     migrations.AddField(model_name='mevent', name='data', field=jsonfield.fields.JSONField(blank=True, verbose_name='Data'))]