# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /mnt/c/django-danceschool/currentmaster/django-danceschool/danceschool/core/migrations/0010_auto_20170720_1643.py
# Compiled at: 2018-03-26 19:55:27
# Size of source mod 2**32: 1020 bytes
from __future__ import unicode_literals
from django.db import migrations, models
import djangocms_text_ckeditor.fields

class Migration(migrations.Migration):
    dependencies = [
     ('core', '0009_auto_20170719_1720')]
    operations = [
     migrations.AlterField(model_name='emailtemplate', name='content', field=models.TextField(blank=True, help_text='See the list of available variables for details on what information can be included with template tags.', null=True, verbose_name='Plain text Content')),
     migrations.AlterField(model_name='emailtemplate', name='html_content', field=djangocms_text_ckeditor.fields.HTMLField(blank=True, help_text='Emails are sent as plain text by default.  To send an HTML email instead, enter your desired content in this field.', null=True, verbose_name='HTML rich text content'))]