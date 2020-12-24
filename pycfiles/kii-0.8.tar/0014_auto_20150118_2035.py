# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/eliotberriot/Seafile/kii/kii_main/kii/stream/migrations/0014_auto_20150118_2035.py
# Compiled at: 2015-01-20 14:25:09
from __future__ import unicode_literals
from django.db import models, migrations

class Migration(migrations.Migration):
    dependencies = [
     ('stream', '0013_auto_20150107_1621')]
    operations = [
     migrations.AlterField(model_name=b'streamitem', name=b'root', field=models.ForeignKey(related_name=b'children', verbose_name=b'stream', to=b'stream.Stream'))]