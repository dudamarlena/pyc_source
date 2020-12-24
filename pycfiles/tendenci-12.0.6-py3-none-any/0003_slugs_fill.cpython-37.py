# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jennyq/.pyenv/versions/venv_t12/lib/python3.7/site-packages/tendenci/apps/forums/migrations/0003_slugs_fill.py
# Compiled at: 2020-03-30 17:48:04
# Size of source mod 2**32: 1348 bytes
from django.db import migrations
from tendenci.apps.forums.models import create_or_check_slug

def fill_slugs(apps, schema_editor):
    Category = apps.get_model('forums', 'Category')
    Forum = apps.get_model('forums', 'Forum')
    Topic = apps.get_model('forums', 'Topic')
    for category in Category.objects.all():
        category.slug = create_or_check_slug(instance=category, model=Category)
        category.save()

    for forum in Forum.objects.all():
        extra_filters = {'category': forum.category}
        forum.slug = create_or_check_slug(instance=forum, model=Forum, **extra_filters)
        forum.save()

    for topic in Topic.objects.all():
        extra_filters = {'forum': topic.forum}
        topic.slug = create_or_check_slug(instance=topic, model=Topic, **extra_filters)
        topic.save()


def clear_slugs(apps, schema_editor):
    Category = apps.get_model('forums', 'Category')
    Forum = apps.get_model('forums', 'Forum')
    Topic = apps.get_model('forums', 'Topic')
    Category.objects.all().update(slug='')
    Forum.objects.all().update(slug='')
    Topic.objects.all().update(slug='')


class Migration(migrations.Migration):
    dependencies = [
     ('forums', '0002_slugs_optional')]
    operations = [
     migrations.RunPython(fill_slugs, clear_slugs)]