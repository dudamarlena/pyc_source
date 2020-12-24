# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/contrib/segments/migrations/0003_segmentsort.py
# Compiled at: 2020-01-05 09:49:45
# Size of source mod 2**32: 1318 bytes
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('basemodels', '0008_auto_20181211_1552'),
     ('segments', '0002_auto_20181026_1745')]
    operations = [
     migrations.CreateModel(name='SegmentSort',
       fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'sort', models.IntegerField(default=0, verbose_name='\\u0645\\u0631\\u062a\\u0628 \\u0633\\u0627\\u0632\\u06cc')),
      (
       'model_obj', models.ForeignKey(on_delete=(django.db.models.deletion.CASCADE), related_name='segment_sort_model', to='basemodels.BaseModel', verbose_name='\\u0686\\u0647 \\u0686\\u06cc\\u0632 \\u0631\\u0627 \\u0646\\u0645\\u0627\\u06cc\\u0634 \\u062f\\u0647\\u062f\\u061f')),
      (
       'segment_obj', models.ForeignKey(on_delete=(django.db.models.deletion.CASCADE), related_name='segment_sort_segment', to='segments.BaseSegment', verbose_name='Segment'))],
       options={'verbose_name':'Segment Sort', 
      'verbose_name_plural':'Segments Sort'})]