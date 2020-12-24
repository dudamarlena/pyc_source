# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mw/dev/pixelcms-server/cms/content/migrations/0008_auto_20161127_1101.py
# Compiled at: 2016-11-27 05:01:13
# Size of source mod 2**32: 461 bytes
from __future__ import unicode_literals
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
     ('content', '0007_auto_20161127_1100')]
    operations = [
     migrations.RenameField(model_name='category', old_name='show_article_contents', new_name='show_articles_contents')]