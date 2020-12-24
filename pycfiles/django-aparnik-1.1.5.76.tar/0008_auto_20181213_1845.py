# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/contrib/segments/migrations/0008_auto_20181213_1845.py
# Compiled at: 2018-12-14 08:14:47
from __future__ import unicode_literals
from django.db import migrations

def create_through_relations(apps, schema_editor):
    Segment = apps.get_model(b'segments', b'BaseSegment')
    PageSort = apps.get_model(b'segments', b'PageSort')
    for obj in Segment.objects.all():
        for page_obj in obj.pages.all():
            PageSort(page_obj=page_obj, segment_obj=obj, sort=0).save()


class Migration(migrations.Migration):
    dependencies = [
     ('segments', '0007_pagesort')]
    operations = [
     migrations.RunPython(create_through_relations, reverse_code=migrations.RunPython.noop)]