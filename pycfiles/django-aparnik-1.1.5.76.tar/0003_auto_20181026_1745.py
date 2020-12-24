# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/contrib/filefields/migrations/0003_auto_20181026_1745.py
# Compiled at: 2018-11-05 07:19:14
from __future__ import unicode_literals
import aparnik.utils.utils
from django.db import migrations, models
import s3direct.fields

class Migration(migrations.Migration):
    dependencies = [
     ('filefields', '0002_auto_20181025_1617')]
    operations = [
     migrations.AlterModelOptions(name=b'filefield', options={b'verbose_name': b'فایل فیلد', b'verbose_name_plural': b'فایل فیلد'}),
     migrations.AlterField(model_name=b'filefield', name=b'file_direct', field=models.FileField(blank=True, null=True, upload_to=aparnik.utils.utils.document_directory_path, verbose_name=b'فایل')),
     migrations.AlterField(model_name=b'filefield', name=b'file_s3', field=s3direct.fields.S3DirectField(blank=True, null=True, verbose_name=b'فایل')),
     migrations.AlterField(model_name=b'filefield', name=b'size', field=models.IntegerField(default=0, verbose_name=b'سایز فایل')),
     migrations.AlterField(model_name=b'filefield', name=b'type', field=models.CharField(choices=[('M', 'فیلم'), ('V', 'صدا'), ('P', 'پی دی اف'), ('I', 'عکس')], max_length=1, verbose_name=b'نوع فایل'))]