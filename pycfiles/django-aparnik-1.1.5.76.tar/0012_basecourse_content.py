# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/packages/educations/courses/migrations/0012_basecourse_content.py
# Compiled at: 2019-04-28 08:05:20
from __future__ import unicode_literals
import ckeditor_uploader.fields
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
     ('courses', '0011_auto_20181214_1330')]
    operations = [
     migrations.AddField(model_name=b'basecourse', name=b'content', field=ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True, verbose_name=b'محتوا'))]