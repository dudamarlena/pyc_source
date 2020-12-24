# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mw/dev/pixelcms-server/cms/content/migrations/0009_auto_20161127_1211.py
# Compiled at: 2016-11-27 06:11:53
# Size of source mod 2**32: 669 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('content', '0008_auto_20161127_1101')]
    operations = [
     migrations.RenameField(model_name='articlesmodule', old_name='show_article_images', new_name='show_articles_images'),
     migrations.AlterField(model_name='category', name='show_article_images', field=models.BooleanField(default=True, verbose_name='show images'))]