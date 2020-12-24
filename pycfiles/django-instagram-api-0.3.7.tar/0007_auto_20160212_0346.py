# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ramusus/workspace/manufacture/env/src/django-instagram-api/instagram_api/migrations/0007_auto_20160212_0346.py
# Compiled at: 2016-02-11 19:46:10
from __future__ import unicode_literals
from django.db import models, migrations

class Migration(migrations.Migration):
    dependencies = [
     ('instagram_api', '0006_media_filter')]
    operations = [
     migrations.RemoveField(model_name=b'location', name=b'media_feed'),
     migrations.RemoveField(model_name=b'tag', name=b'media_feed'),
     migrations.AddField(model_name=b'media', name=b'locations', field=models.ManyToManyField(related_name=b'media_feed', to=b'instagram_api.Location'), preserve_default=True),
     migrations.AddField(model_name=b'media', name=b'tags', field=models.ManyToManyField(related_name=b'media_feed', to=b'instagram_api.Tag'), preserve_default=True)]