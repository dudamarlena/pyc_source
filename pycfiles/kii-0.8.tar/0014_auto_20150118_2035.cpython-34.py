# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/eliotberriot/Seafile/kii/kii_main/kii/stream/migrations/0014_auto_20150118_2035.py
# Compiled at: 2015-01-18 14:35:33
# Size of source mod 2**32: 457 bytes
from __future__ import unicode_literals
from django.db import models, migrations

class Migration(migrations.Migration):
    dependencies = [
     ('stream', '0013_auto_20150107_1621')]
    operations = [
     migrations.AlterField(model_name='streamitem', name='root', field=models.ForeignKey(related_name='children', verbose_name='stream', to='stream.Stream'))]