# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/contrib/filefields/migrations/0011_auto_20190615_1430.py
# Compiled at: 2020-01-05 09:49:45
# Size of source mod 2**32: 2024 bytes
import aparnik.utils.utils
from django.db import migrations, models
import s3direct.fields

class Migration(migrations.Migration):
    dependencies = [
     ('filefields', '0010_filefield_is_decrypt_needed')]
    operations = [
     migrations.AlterModelOptions(name='filefield',
       options={'verbose_name':'فایل فیلد', 
      'verbose_name_plural':'فایل فیلد'}),
     migrations.AlterField(model_name='filefield',
       name='file_direct',
       field=models.FileField(blank=True, null=True, upload_to=(aparnik.utils.utils.document_directory_path), verbose_name='فایل')),
     migrations.AlterField(model_name='filefield',
       name='file_s3',
       field=s3direct.fields.S3DirectField(blank=True, null=True, verbose_name='فایل')),
     migrations.AlterField(model_name='filefield',
       name='password',
       field=models.CharField(blank=True, default='', max_length=64, null=True, verbose_name='گذرواژه')),
     migrations.AlterField(model_name='filefield',
       name='seconds',
       field=models.BigIntegerField(default=0, verbose_name='زمان')),
     migrations.AlterField(model_name='filefield',
       name='size',
       field=models.IntegerField(default=0, verbose_name='سایز فایل')),
     migrations.AlterField(model_name='filefield',
       name='title',
       field=models.CharField(blank=True, max_length=100, null=True, verbose_name='عنوان')),
     migrations.AlterField(model_name='filefield',
       name='type',
       field=models.CharField(blank=True, choices=[('M', 'فیلم'), ('V', 'صدا'), ('P', 'پی دی اف'), ('I', 'عکس')], max_length=1, null=True, verbose_name='نوع فایل'))]