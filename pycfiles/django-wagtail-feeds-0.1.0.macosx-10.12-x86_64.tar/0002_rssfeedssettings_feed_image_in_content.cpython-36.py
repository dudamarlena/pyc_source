# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/site-packages/wagtail_feeds/migrations/0002_rssfeedssettings_feed_image_in_content.py
# Compiled at: 2018-05-08 10:24:10
# Size of source mod 2**32: 525 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('wagtail_feeds', '0001_initial')]
    operations = [
     migrations.AddField(model_name='rssfeedssettings',
       name='feed_image_in_content',
       field=models.BooleanField(default=True, help_text=b'Add feed image to content encoded field'))]