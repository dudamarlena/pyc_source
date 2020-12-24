# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/helpcenter/migrations/0009_category_slug_squashed_0011_auto_20160928_0840.py
# Compiled at: 2016-09-30 00:56:02
from __future__ import unicode_literals
from django.db import migrations, models
import django.db.migrations.operations.special
from django.utils.text import slugify

def create_slugs(apps, schema_editor):
    """Create slugs for existing categories."""
    Category = apps.get_model(b'helpcenter', b'Category')
    for category in Category.objects.all():
        slug = slugify(category.title)[:50]
        category.slug = slug
        category.save()


class Migration(migrations.Migration):
    dependencies = [
     ('helpcenter', '0008_article_draft')]
    operations = [
     migrations.AddField(model_name=b'category', name=b'slug', field=models.SlugField(null=True, verbose_name=b'Category URL Slug')),
     migrations.RunPython(code=create_slugs, reverse_code=migrations.RunPython.noop),
     migrations.AlterField(model_name=b'category', name=b'slug', field=models.SlugField(verbose_name=b'Category URL Slug'))]