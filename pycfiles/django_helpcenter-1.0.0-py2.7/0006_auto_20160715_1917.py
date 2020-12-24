# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/helpcenter/migrations/0006_auto_20160715_1917.py
# Compiled at: 2016-09-30 00:56:02
from __future__ import unicode_literals
from django.db import migrations

def add_edit_time(apps, schema_editor):
    """ Add edit_time to all existing Article instances """
    Article = apps.get_model(b'helpcenter', b'Article')
    for article in Article.objects.all():
        if not article.time_edited:
            article.time_edited = article.time_published
        article.save()


class Migration(migrations.Migration):
    dependencies = [
     ('helpcenter', '0005_article_time_edited')]
    operations = [
     migrations.RunPython(add_edit_time)]