# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/contrib/segments/migrations/0004_auto_20181213_1607.py
# Compiled at: 2020-01-05 09:49:45
# Size of source mod 2**32: 733 bytes
from django.db import migrations

def create_through_relations(apps, schema_editor):
    Segment = apps.get_model('segments', 'BaseSegment')
    SegmentSort = apps.get_model('segments', 'SegmentSort')
    for obj in Segment.objects.all():
        for model_obj in obj.model_obj.all():
            SegmentSort(model_obj=model_obj,
              segment_obj=obj,
              sort=0).save()


class Migration(migrations.Migration):
    dependencies = [
     ('segments', '0003_segmentsort')]
    operations = [
     migrations.RunPython(create_through_relations, reverse_code=(migrations.RunPython.noop))]