# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ramusus/workspace/manufacture/env/src/django-instagram-api/instagram_api/migrations/0011_auto_20160213_0338.py
# Compiled at: 2016-02-12 20:59:08
from __future__ import unicode_literals
from django.db import models, migrations

class Migration(migrations.Migration):
    dependencies = [
     ('instagram_api', '0010_auto_20160212_1602')]
    operations = [
     migrations.AlterField(model_name=b'media', name=b'link', field=models.URLField(max_length=68), preserve_default=True),
     migrations.AlterField(model_name=b'media', name=b'remote_id', field=models.CharField(unique=True, max_length=30), preserve_default=True),
     migrations.AlterField(model_name=b'media', name=b'type', field=models.CharField(max_length=5), preserve_default=True),
     migrations.AlterField(model_name=b'media', name=b'video_low_bandwidth', field=models.URLField(max_length=130), preserve_default=True),
     migrations.AlterField(model_name=b'media', name=b'video_low_resolution', field=models.URLField(max_length=130), preserve_default=True),
     migrations.AlterField(model_name=b'media', name=b'video_standard_resolution', field=models.URLField(max_length=130), preserve_default=True),
     migrations.AlterField(model_name=b'user', name=b'bio', field=models.CharField(max_length=150), preserve_default=True),
     migrations.AlterField(model_name=b'user', name=b'full_name', field=models.CharField(max_length=30), preserve_default=True),
     migrations.AlterField(model_name=b'user', name=b'profile_picture', field=models.URLField(max_length=112), preserve_default=True),
     migrations.AlterField(model_name=b'user', name=b'username', field=models.CharField(unique=True, max_length=30), preserve_default=True),
     migrations.AlterField(model_name=b'user', name=b'website', field=models.URLField(max_length=150), preserve_default=True)]