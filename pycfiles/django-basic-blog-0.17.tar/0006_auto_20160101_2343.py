# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ben/Projects/django-basic-blog/blog/migrations/0006_auto_20160101_2343.py
# Compiled at: 2016-01-01 18:43:28
from __future__ import unicode_literals
from django.db import migrations, models
import taggit.managers

class Migration(migrations.Migration):
    dependencies = [
     ('taggit', '0002_auto_20150616_2121'),
     ('blog', '0005_entry_description')]
    operations = [
     migrations.AddField(model_name=b'entry', name=b'script', field=models.TextField(blank=True, null=True)),
     migrations.AddField(model_name=b'entry', name=b'tags', field=taggit.managers.TaggableManager(help_text=b'A comma-separated list of tags.', through=b'taggit.TaggedItem', to=b'taggit.Tag', verbose_name=b'Tags'))]