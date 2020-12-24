# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/contrib/filefields/migrations/0015_auto_20200316_1110.py
# Compiled at: 2020-03-16 03:40:40
# Size of source mod 2**32: 1964 bytes
import aparnik.utils.utils
from django.db import migrations, models
import s3direct.fields

class Migration(migrations.Migration):
    dependencies = [
     ('filefields', '0014_auto_20200210_1451')]
    operations = [
     migrations.AlterModelOptions(name='filefield',
       options={'verbose_name':'File Field', 
      'verbose_name_plural':'Files Field'}),
     migrations.AlterField(model_name='filefield',
       name='file_direct',
       field=models.FileField(blank=True, null=True, upload_to=(aparnik.utils.utils.document_directory_path), verbose_name='File')),
     migrations.AlterField(model_name='filefield',
       name='file_s3',
       field=s3direct.fields.S3DirectField(blank=True, null=True, verbose_name='File')),
     migrations.AlterField(model_name='filefield',
       name='password',
       field=models.CharField(blank=True, default='', max_length=64, null=True, verbose_name='Password')),
     migrations.AlterField(model_name='filefield',
       name='seconds',
       field=models.BigIntegerField(default=0, verbose_name='Time')),
     migrations.AlterField(model_name='filefield',
       name='size',
       field=models.IntegerField(default=0, verbose_name='File Size')),
     migrations.AlterField(model_name='filefield',
       name='title',
       field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Title')),
     migrations.AlterField(model_name='filefield',
       name='type',
       field=models.CharField(blank=True, choices=[('M', 'Movie'), ('V', 'Voice'), ('P', 'PDF'), ('I', 'Image'), ('L', 'Link')], max_length=1, null=True, verbose_name='File Type'))]