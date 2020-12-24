# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ramusus/workspace/manufacture/env/src/django-instagram-api/instagram_api/migrations/0009_auto_20160212_1454.py
# Compiled at: 2016-02-12 06:54:39
from __future__ import unicode_literals
from django.db import models, migrations

class Migration(migrations.Migration):
    dependencies = [
     ('instagram_api', '0008_auto_20160212_1345')]
    operations = [
     migrations.RemoveField(model_name=b'media', name=b'locations'),
     migrations.AddField(model_name=b'media', name=b'location', field=models.ForeignKey(related_name=b'media_feed', to=b'instagram_api.Location', null=True), preserve_default=True)]