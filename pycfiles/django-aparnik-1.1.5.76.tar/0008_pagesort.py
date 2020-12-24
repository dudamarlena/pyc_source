# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/contrib/segments/migrations/0008_pagesort.py
# Compiled at: 2018-12-13 07:50:53
from __future__ import unicode_literals
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('basemodels', '0008_auto_20181211_1552'),
     ('segments', '0007_remove_basesegment_sort')]
    operations = [
     migrations.CreateModel(name=b'PageSort', fields=[
      (
       b'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name=b'ID')),
      (
       b'sort', models.IntegerField(default=0, verbose_name=b'مرتب سازی')),
      (
       b'model_obj', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name=b'page_sort_model', to=b'basemodels.BaseModel', verbose_name=b'چه چیز را نمایش دهد؟')),
      (
       b'page_obj', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name=b'page_sort_segment', to=b'segments.BaseSegment', verbose_name=b'صفحه'))], options={b'verbose_name': b'Page Sort', 
        b'verbose_name_plural': b'Pages Sort'})]