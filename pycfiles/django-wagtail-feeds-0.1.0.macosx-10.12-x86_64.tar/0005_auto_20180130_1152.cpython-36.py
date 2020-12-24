# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/site-packages/wagtail_feeds/migrations/0005_auto_20180130_1152.py
# Compiled at: 2018-05-08 10:24:10
# Size of source mod 2**32: 484 bytes
from __future__ import unicode_literals
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
     ('wagtail_feeds', '0004_auto_20180130_0948')]
    operations = [
     migrations.AlterModelOptions(name='rssfeedssettings',
       options={'verbose_name':'RSS feed setting', 
      'verbose_name_plural':'RSS feed settings'})]