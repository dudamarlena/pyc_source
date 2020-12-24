# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/eetu/envs/cmsplugin-articles-ai/project/cmsplugin_articles_ai/migrations/0004_data_migration_for_slug_field.py
# Compiled at: 2017-07-21 05:10:28
# Size of source mod 2**32: 552 bytes
from __future__ import unicode_literals
from django.db import migrations, models
from django.utils.text import slugify

def assign_slug_field(apps, schema_editor):
    Tag = apps.get_model('cmsplugin_articles_ai', 'Tag')
    for tag in Tag.objects.all():
        tag.slug = slugify(tag.name)
        tag.save()


class Migration(migrations.Migration):
    dependencies = [
     ('cmsplugin_articles_ai', '0003_add_non_unique_slug_to_tags')]
    operations = [
     migrations.RunPython(assign_slug_field)]