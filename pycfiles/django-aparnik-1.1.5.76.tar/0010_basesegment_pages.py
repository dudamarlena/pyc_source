# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/contrib/segments/migrations/0010_basesegment_pages.py
# Compiled at: 2018-12-14 08:14:47
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('pages', '0002_page_english_title'),
     ('segments', '0009_remove_basesegment_pages')]
    operations = [
     migrations.AddField(model_name=b'basesegment', name=b'pages', field=models.ManyToManyField(blank=True, related_name=b'segment_pages', through=b'segments.PageSort', to=b'pages.Page', verbose_name=b'صفحه'))]