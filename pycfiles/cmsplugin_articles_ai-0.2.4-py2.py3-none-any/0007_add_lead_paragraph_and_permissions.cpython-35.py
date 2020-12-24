# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/eetu/envs/cmsplugin-articles-ai/project/cmsplugin_articles_ai/migrations/0007_add_lead_paragraph_and_permissions.py
# Compiled at: 2017-07-21 05:10:28
# Size of source mod 2**32: 767 bytes
from __future__ import unicode_literals
from django.db import migrations, models
import djangocms_text_ckeditor.fields

class Migration(migrations.Migration):
    dependencies = [
     ('cmsplugin_articles_ai', '0006_add_publisher_support')]
    operations = [
     migrations.AlterModelOptions(name='article', options={'permissions': (('can_publish', 'Can publish'), ), 'verbose_name_plural': 'articles', 'ordering': ('-published_from', '-pk'), 'verbose_name': 'article'}),
     migrations.AddField(model_name='article', name='lead_paragraph', field=djangocms_text_ckeditor.fields.HTMLField(blank=True, verbose_name='lead paragraph'))]