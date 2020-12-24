# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dominicmonn/Documents/Private/cms-sample/dev_packages/djangocms-career/djangocms_career/migrations/0007_auto_20160418_1325.py
# Compiled at: 2016-04-18 07:25:54
from __future__ import unicode_literals
from django.db import migrations, models
import djangocms_text_ckeditor.fields

class Migration(migrations.Migration):
    dependencies = [
     ('djangocms_career', '0006_remove_post_is_public')]
    operations = [
     migrations.AlterField(model_name=b'post', name=b'description', field=djangocms_text_ckeditor.fields.HTMLField(help_text=b'Give a short description about your work and responsibilities.', max_length=2048, null=True, verbose_name=b'Description', blank=True))]