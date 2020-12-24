# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/nodeconductor_saltstack/sharepoint/migrations/0002_site_tags.py
# Compiled at: 2016-09-28 02:05:53
from __future__ import unicode_literals
from django.db import models, migrations
import taggit.managers

class Migration(migrations.Migration):
    dependencies = [
     ('taggit', '0002_auto_20150616_2121'),
     ('sharepoint', '0001_initial')]
    operations = [
     migrations.AddField(model_name=b'site', name=b'tags', field=taggit.managers.TaggableManager(to=b'taggit.Tag', through=b'taggit.TaggedItem', help_text=b'A comma-separated list of tags.', verbose_name=b'Tags', blank=True), preserve_default=True)]