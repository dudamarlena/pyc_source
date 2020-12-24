# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/cameronlowe/Development/django-zencoder/zencoder/migrations/0002_add_video_duration.py
# Compiled at: 2015-07-14 20:28:02
# Size of source mod 2**32: 445 bytes
from __future__ import unicode_literals
from django.db import models, migrations

class Migration(migrations.Migration):
    dependencies = [
     ('zencoder', '0001_initial')]
    operations = [
     migrations.AddField(model_name='video', name='duration', field=models.PositiveIntegerField(blank=True, default=0), preserve_default=True)]