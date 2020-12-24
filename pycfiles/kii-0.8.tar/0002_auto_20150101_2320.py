# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/eliotberriot/Seafile/kii/kii_main/kii/classify/migrations/0002_auto_20150101_2320.py
# Compiled at: 2015-01-01 17:22:32
from __future__ import unicode_literals
from django.db import models, migrations

class Migration(migrations.Migration):
    dependencies = [
     ('classify', '0001_initial')]
    operations = [
     migrations.AlterField(model_name=b'tag', name=b'title', field=models.CharField(max_length=255, verbose_name=b'Title'))]