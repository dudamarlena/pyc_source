# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/eetu/envs/cmsplugin-articles-ai/project/cmsplugin_articles_ai/migrations/0002_add_language_fields.py
# Compiled at: 2017-07-21 05:10:28
# Size of source mod 2**32: 1004 bytes
from __future__ import unicode_literals
from django.db import migrations, models
import softchoice.fields.language

class Migration(migrations.Migration):
    dependencies = [
     ('cmsplugin_articles_ai', '0001_initial')]
    operations = [
     migrations.AddField(model_name='article', name='language', field=softchoice.fields.language.LanguageField(help_text='Leave this empty if you want the article to be shown regardless of any language filters.', blank=True, verbose_name='language', max_length=10)),
     migrations.AddField(model_name='articlelistplugin', name='language_filter', field=softchoice.fields.language.LanguageField(help_text="Select a language if you want to list only articles written in specificlanguage. If you don't select a language, the listing includes all languages.", blank=True, verbose_name='language filter', max_length=10))]