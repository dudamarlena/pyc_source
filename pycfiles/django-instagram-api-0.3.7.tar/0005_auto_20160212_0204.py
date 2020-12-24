# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ramusus/workspace/manufacture/env/src/django-instagram-api/instagram_api/migrations/0005_auto_20160212_0204.py
# Compiled at: 2016-02-11 18:04:26
from __future__ import unicode_literals
from django.db import models, migrations

class Migration(migrations.Migration):
    dependencies = [
     ('instagram_api', '0004_location')]
    operations = [
     migrations.AlterField(model_name=b'location', name=b'latitude', field=models.FloatField(null=True), preserve_default=True),
     migrations.AlterField(model_name=b'location', name=b'longitude', field=models.FloatField(null=True), preserve_default=True)]