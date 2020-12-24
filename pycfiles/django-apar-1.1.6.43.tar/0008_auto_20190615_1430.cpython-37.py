# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/packages/shops/files/migrations/0008_auto_20190615_1430.py
# Compiled at: 2020-01-05 09:49:45
# Size of source mod 2**32: 1751 bytes
from django.db import migrations, models
import django.db.models.deletion, django.utils.timezone

class Migration(migrations.Migration):
    dependencies = [
     ('files', '0007_auto_20190501_1147')]
    operations = [
     migrations.AlterModelOptions(name='file',
       options={'ordering':[
       '-created_at'], 
      'verbose_name':'فایل',  'verbose_name_plural':'فایل ها'}),
     migrations.AlterField(model_name='file',
       name='banner',
       field=models.ForeignKey(blank=True, null=True, on_delete=(django.db.models.deletion.CASCADE), related_name='shop_file_banner', to='filefields.FileField', verbose_name='بنر')),
     migrations.AlterField(model_name='file',
       name='cover',
       field=models.ForeignKey(blank=True, null=True, on_delete=(django.db.models.deletion.CASCADE), related_name='shop_file_cover', to='filefields.FileField', verbose_name='تصویر جلد')),
     migrations.AlterField(model_name='file',
       name='description',
       field=models.TextField(blank=True, null=True, verbose_name='توضیحات')),
     migrations.AlterField(model_name='file',
       name='file_obj',
       field=models.ForeignKey(on_delete=(django.db.models.deletion.CASCADE), related_name='shop_file_obj', to='filefields.FileField', verbose_name='فایل')),
     migrations.AlterField(model_name='file',
       name='publish_date',
       field=models.DateTimeField(default=(django.utils.timezone.now), verbose_name='تاریخ انتشار'))]