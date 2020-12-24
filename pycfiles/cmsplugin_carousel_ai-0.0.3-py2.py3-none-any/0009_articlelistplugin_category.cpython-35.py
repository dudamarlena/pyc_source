# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/eetu/envs/cmsplugin-articles-ai/project/cmsplugin_articles_ai/migrations/0009_articlelistplugin_category.py
# Compiled at: 2017-07-21 08:11:35
# Size of source mod 2**32: 508 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('cmsplugin_articles_ai', '0008_categories')]
    operations = [
     migrations.AddField(model_name='articlelistplugin', name='category', field=models.ForeignKey(related_name='+', blank=True, null=True, to='cmsplugin_articles_ai.Category', verbose_name='category'))]