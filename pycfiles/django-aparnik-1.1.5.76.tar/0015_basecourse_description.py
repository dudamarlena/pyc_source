# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/packages/educations/courses/migrations/0015_basecourse_description.py
# Compiled at: 2019-04-28 08:16:36
from __future__ import unicode_literals
import ckeditor_uploader.fields
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
     ('courses', '0014_remove_basecourse_description')]
    operations = [
     migrations.AddField(model_name=b'basecourse', name=b'description', field=ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True, verbose_name=b'توضیحات'))]