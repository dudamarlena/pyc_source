# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/eliotberriot/Seafile/kii/kii_main/kii/stream/migrations/0006_auto_20141217_1757.py
# Compiled at: 2015-01-17 16:40:50
from __future__ import unicode_literals
from django.db import models, migrations

class Migration(migrations.Migration):
    dependencies = [
     ('stream', '0005_auto_20141217_1455')]
    operations = [
     migrations.AlterField(model_name=b'itemcomment', name=b'status', field=models.CharField(default=b'pub', max_length=5, choices=[('dra', 'base_models.status_mixin.draft'), ('pub', 'base_models.status_mixin.published')])),
     migrations.AlterField(model_name=b'streamitem', name=b'status', field=models.CharField(default=b'pub', max_length=5, choices=[('dra', 'base_models.status_mixin.draft'), ('pub', 'base_models.status_mixin.published')]))]