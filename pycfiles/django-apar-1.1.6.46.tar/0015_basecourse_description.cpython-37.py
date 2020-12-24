# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/packages/educations/courses/migrations/0015_basecourse_description.py
# Compiled at: 2020-01-05 09:49:45
# Size of source mod 2**32: 559 bytes
import ckeditor_uploader.fields
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
     ('courses', '0014_remove_basecourse_description')]
    operations = [
     migrations.AddField(model_name='basecourse',
       name='description',
       field=ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True, verbose_name='\\u062a\\u0648\\u0636\\u06cc\\u062d\\u0627\\u062a'))]