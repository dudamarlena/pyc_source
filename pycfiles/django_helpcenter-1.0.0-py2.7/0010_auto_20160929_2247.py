# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/helpcenter/migrations/0010_auto_20160929_2247.py
# Compiled at: 2016-09-30 00:56:02
from __future__ import unicode_literals
from django.db import migrations, models
from django.utils.text import slugify

def create_article_slugs(apps, schema_editor):
    """Create slugs for existing articles."""
    Article = apps.get_model(b'helpcenter', b'Article')
    for article in Article.objects.all():
        slug = slugify(article.title)[:50]
        article.slug = slug
        article.save()


class Migration(migrations.Migration):
    dependencies = [
     ('helpcenter', '0009_category_slug_squashed_0011_auto_20160928_0840')]
    operations = [
     migrations.AddField(model_name=b'article', name=b'slug', field=models.SlugField(null=True, verbose_name=b'Article URL Slug')),
     migrations.RunPython(code=create_article_slugs, reverse_code=migrations.RunPython.noop),
     migrations.AlterField(model_name=b'article', name=b'slug', field=models.SlugField(verbose_name=b'Article URL Slug'))]