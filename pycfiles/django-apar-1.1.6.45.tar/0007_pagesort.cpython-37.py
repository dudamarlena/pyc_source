# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/contrib/segments/migrations/0007_pagesort.py
# Compiled at: 2020-01-05 09:49:45
# Size of source mod 2**32: 1201 bytes
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('pages', '0002_page_english_title'),
     ('segments', '0006_basesegment_model_obj')]
    operations = [
     migrations.CreateModel(name='PageSort',
       fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'sort', models.IntegerField(default=0, verbose_name='\\u0645\\u0631\\u062a\\u0628 \\u0633\\u0627\\u0632\\u06cc')),
      (
       'page_obj', models.ForeignKey(on_delete=(django.db.models.deletion.CASCADE), related_name='page_sort_page', to='pages.Page', verbose_name='\\u0635\\u0641\\u062d\\u0647')),
      (
       'segment_obj', models.ForeignKey(on_delete=(django.db.models.deletion.CASCADE), related_name='page_sort_segment', to='segments.BaseSegment', verbose_name='Segment'))],
       options={'verbose_name':'Page Sort', 
      'verbose_name_plural':'Pages Sort'})]