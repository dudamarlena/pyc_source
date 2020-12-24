# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/eetu/envs/cmsplugin-articles-ai/project/cmsplugin_articles_ai/migrations/0005_make_tag_slug_field_unique.py
# Compiled at: 2017-07-21 05:10:28
# Size of source mod 2**32: 457 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('cmsplugin_articles_ai', '0004_data_migration_for_slug_field')]
    operations = [
     migrations.AlterField(model_name='tag', name='slug', field=models.SlugField(unique=True, verbose_name='slug', max_length=200))]