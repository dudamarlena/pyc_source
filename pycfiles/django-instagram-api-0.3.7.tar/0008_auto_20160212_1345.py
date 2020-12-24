# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ramusus/workspace/manufacture/env/src/django-instagram-api/instagram_api/migrations/0008_auto_20160212_1345.py
# Compiled at: 2016-02-12 05:45:18
from __future__ import unicode_literals
from django.db import models, migrations

class Migration(migrations.Migration):
    dependencies = [
     ('instagram_api', '0007_auto_20160212_0346')]
    operations = [
     migrations.RemoveField(model_name=b'location', name=b'street_address'),
     migrations.AlterField(model_name=b'tag', name=b'name', field=models.CharField(unique=True, max_length=50), preserve_default=True)]