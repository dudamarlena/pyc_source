# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/eetu/envs/cmsplugin-articles-ai/project/cmsplugin_articles_ai/migrations/0008_categories.py
# Compiled at: 2017-08-31 05:41:42
# Size of source mod 2**32: 1438 bytes
from __future__ import unicode_literals
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('cmsplugin_articles_ai', '0007_add_lead_paragraph_and_permissions')]
    operations = [
     migrations.CreateModel(name='Category', fields=[
      (
       'id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
      (
       'title', models.CharField(max_length=200, verbose_name='title')),
      (
       'slug', models.SlugField(unique=True, max_length=200, verbose_name='URL slug'))], options={'ordering': ['title'], 
      'verbose_name': 'category', 
      'verbose_name_plural': 'categories'}),
     migrations.AddField(model_name='article', name='category', field=models.ForeignKey(related_name='articles', blank=True, on_delete=django.db.models.deletion.SET_NULL, null=True, verbose_name='category', to='cmsplugin_articles_ai.Category')),
     migrations.AddField(model_name='articlelistplugin', name='category', field=models.ForeignKey(related_name='+', blank=True, null=True, verbose_name='category', to='cmsplugin_articles_ai.Category'))]