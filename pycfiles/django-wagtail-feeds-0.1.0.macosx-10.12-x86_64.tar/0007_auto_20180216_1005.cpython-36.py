# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/site-packages/wagtail_feeds/migrations/0007_auto_20180216_1005.py
# Compiled at: 2018-05-08 10:24:10
# Size of source mod 2**32: 602 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('wagtail_feeds', '0006_auto_20180216_0933')]
    operations = [
     migrations.AlterField(model_name='rssfeedssettings',
       name='feed_item_date_field',
       field=models.CharField(blank=True, help_text='(Optional). Date Field for feed item. By default use date', max_length=255, verbose_name='Feed item date field'))]