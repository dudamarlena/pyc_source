# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/eetu/envs/cmsplugin-articles-ai/project/cmsplugin_articles_ai/migrations/0003_add_non_unique_slug_to_tags.py
# Compiled at: 2017-07-21 05:10:28
# Size of source mod 2**32: 444 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('cmsplugin_articles_ai', '0002_add_language_fields')]
    operations = [
     migrations.AddField(model_name='tag', name='slug', field=models.SlugField(verbose_name='slug', blank=True, max_length=200))]