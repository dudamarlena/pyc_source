# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/packages/news/migrations/0006_auto_20190615_1430.py
# Compiled at: 2020-01-05 09:49:45
# Size of source mod 2**32: 1412 bytes
import ckeditor_uploader.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion, django.utils.timezone

class Migration(migrations.Migration):
    dependencies = [
     ('news', '0005_auto_20181210_1511')]
    operations = [
     migrations.AlterField(model_name='news',
       name='categories',
       field=models.ManyToManyField(blank=True, to='categories.Category', verbose_name='دسته بندی ها')),
     migrations.AlterField(model_name='news',
       name='content',
       field=ckeditor_uploader.fields.RichTextUploadingField(verbose_name='محتوا')),
     migrations.AlterField(model_name='news',
       name='publish_date',
       field=models.DateTimeField(default=(django.utils.timezone.now), verbose_name='تاریخ انتشار')),
     migrations.AlterField(model_name='news',
       name='title',
       field=models.CharField(max_length=200, verbose_name='عنوان')),
     migrations.AlterField(model_name='news',
       name='user_obj',
       field=models.ForeignKey(on_delete=(django.db.models.deletion.CASCADE), to=(settings.AUTH_USER_MODEL), verbose_name='کاربر'))]