# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/contrib/segments/migrations/0013_auto_20190615_1430.py
# Compiled at: 2020-01-05 09:49:45
# Size of source mod 2**32: 2708 bytes
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('segments', '0012_auto_20181214_1330')]
    operations = [
     migrations.AlterModelOptions(name='basesegment',
       options={'verbose_name':'بخش پایه', 
      'verbose_name_plural':'بخش پایه'}),
     migrations.AlterField(model_name='basesegment',
       name='created_at',
       field=models.DateTimeField(auto_now_add=True, verbose_name='ساخته شده در')),
     migrations.AlterField(model_name='basesegment',
       name='is_active',
       field=models.BooleanField(default=True, verbose_name='فعال؟')),
     migrations.AlterField(model_name='basesegment',
       name='model_obj',
       field=models.ManyToManyField(through='segments.SegmentSort', to='basemodels.BaseModel', verbose_name='چه چیز را نمایش دهد؟')),
     migrations.AlterField(model_name='basesegment',
       name='pages',
       field=models.ManyToManyField(blank=True, related_name='segment_pages', through='segments.PageSort', to='pages.Page', verbose_name='صفحه')),
     migrations.AlterField(model_name='basesegment',
       name='title',
       field=models.CharField(max_length=60, verbose_name='عنوان')),
     migrations.AlterField(model_name='basesegment',
       name='update_at',
       field=models.DateTimeField(auto_now=True, verbose_name='بروزرسانی شده در')),
     migrations.AlterField(model_name='pagesort',
       name='page_obj',
       field=models.ForeignKey(on_delete=(django.db.models.deletion.CASCADE), related_name='page_sort_page', to='pages.Page', verbose_name='صفحه')),
     migrations.AlterField(model_name='pagesort',
       name='sort',
       field=models.IntegerField(default=0, verbose_name='مرتب سازی')),
     migrations.AlterField(model_name='segmentsort',
       name='model_obj',
       field=models.ForeignKey(on_delete=(django.db.models.deletion.CASCADE), related_name='segment_sort_model', to='basemodels.BaseModel', verbose_name='چه چیز را نمایش دهد؟')),
     migrations.AlterField(model_name='segmentsort',
       name='sort',
       field=models.IntegerField(default=0, verbose_name='مرتب سازی'))]