# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /c/Users/Lee/Sync/projects/django-danceschool/currentmaster/django-danceschool/danceschool/core/migrations/0009_auto_20170719_1720.py
# Compiled at: 2019-04-03 22:56:25
# Size of source mod 2**32: 989 bytes
from __future__ import unicode_literals
from django.db import migrations, models
import djangocms_text_ckeditor.fields

class Migration(migrations.Migration):
    dependencies = [
     ('core', '0008_auto_20170717_1642')]
    operations = [
     migrations.AddField(model_name='emailtemplate',
       name='html_content',
       field=djangocms_text_ckeditor.fields.HTMLField(blank=True, help_text='Emails are sent as plain text by default.  To send an HTML email instead, enter your desired content in this field.', null=True, verbose_name='HTML Rich Text content')),
     migrations.AddField(model_name='emailtemplate',
       name='richTextChoice',
       field=models.CharField(choices=[('plain', 'Plain text email'), ('HTML', 'HTML rich text email')], default='plain', max_length=5, verbose_name='Send this email as'))]