# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ramusus/workspace/manufacture/env/src/django-instagram-api/instagram_api/migrations/0006_media_filter.py
# Compiled at: 2016-02-11 19:20:39
from __future__ import unicode_literals
from django.db import models, migrations

class Migration(migrations.Migration):
    dependencies = [
     ('instagram_api', '0005_auto_20160212_0204')]
    operations = [
     migrations.AddField(model_name=b'media', name=b'filter', field=models.CharField(default=b'', max_length=40), preserve_default=False)]