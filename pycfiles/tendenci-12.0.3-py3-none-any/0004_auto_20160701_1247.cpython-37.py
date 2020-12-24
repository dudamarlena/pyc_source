# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jennyq/.pyenv/versions/venv_t12/lib/python3.7/site-packages/tendenci/apps/news/migrations/0004_auto_20160701_1247.py
# Compiled at: 2020-03-30 17:48:04
# Size of source mod 2**32: 578 bytes
from django.db import migrations

def news_group_to_groups(apps, schema_editor):
    """
        Migrate event.group foreignkey relationship to the
        many-to-many relationship in event.groups
    """
    News = apps.get_model('news', 'News')
    for my_news in News.objects.all():
        if my_news.group:
            my_news.groups.add(my_news.group)


class Migration(migrations.Migration):
    dependencies = [
     ('news', '0003_auto_20160701_1246')]
    operations = [
     migrations.RunPython(news_group_to_groups)]