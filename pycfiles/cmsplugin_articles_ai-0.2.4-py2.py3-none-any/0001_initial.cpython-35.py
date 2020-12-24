# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/eetu/envs/cmsplugin-articles-ai/project/cmsplugin_articles_ai/migrations/0001_initial.py
# Compiled at: 2017-07-21 05:10:28
# Size of source mod 2**32: 4645 bytes
from __future__ import unicode_literals
from django.db import migrations, models
import enumfields.fields, djangocms_text_ckeditor.fields, filer.fields.image
from django.conf import settings
import cmsplugin_articles_ai.models, filer.fields.file, django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('filer', '0006_auto_20160623_1627'),
     migrations.swappable_dependency(settings.AUTH_USER_MODEL),
     ('cms', '0016_auto_20160608_1535')]
    operations = [
     migrations.CreateModel(name='Article', fields=[
      (
       'id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
      (
       'title', models.CharField(max_length=200, verbose_name='title')),
      (
       'slug', models.SlugField(max_length=200, verbose_name='URL slug')),
      (
       'published_from', models.DateTimeField(null=True, blank=True, verbose_name='published from')),
      (
       'published_until', models.DateTimeField(null=True, blank=True, verbose_name='published until')),
      (
       'highlight', models.BooleanField(default=False, help_text='Highlight as important.', verbose_name='highlight')),
      (
       'main_content', djangocms_text_ckeditor.fields.HTMLField(verbose_name='content')),
      (
       'created_at', models.DateTimeField(auto_now_add=True, verbose_name='creation time')),
      (
       'modified_at', models.DateTimeField(auto_now=True, verbose_name='last modified')),
      (
       'author', models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=django.db.models.deletion.PROTECT, verbose_name='author')),
      (
       'main_image', filer.fields.image.FilerImageField(on_delete=django.db.models.deletion.SET_NULL, to='filer.Image', related_name='+', null=True, blank=True, verbose_name='main image'))], options={'verbose_name_plural': 'articles', 
      'ordering': ('-published_from', '-pk'), 
      'verbose_name': 'article'}),
     migrations.CreateModel(name='ArticleAttachment', fields=[
      (
       'id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
      (
       'name', models.CharField(max_length=64, blank=True, verbose_name='name')),
      (
       'is_image', models.BooleanField(db_index=True, editable=False, default=False)),
      (
       'article', models.ForeignKey(related_name='attachments', to='cmsplugin_articles_ai.Article', verbose_name='article')),
      (
       'attachment_file', filer.fields.file.FilerFileField(to='filer.File', on_delete=models.SET(''), verbose_name='file'))], options={'verbose_name_plural': 'article attachments', 
      'verbose_name': 'article attachment'}),
     migrations.CreateModel(name='ArticleListPlugin', fields=[
      (
       'cmsplugin_ptr', models.OneToOneField(related_name='cmsplugin_articles_ai_articlelistplugin', primary_key=True, parent_link=True, to='cms.CMSPlugin', auto_created=True, serialize=False)),
      (
       'filter_mode', enumfields.fields.EnumIntegerField(default=1, enum=cmsplugin_articles_ai.models.TagFilterMode, verbose_name='filter')),
      (
       'article_amount', models.PositiveSmallIntegerField(default=5, verbose_name='amount of articles'))], options={'abstract': False}, bases=('cms.cmsplugin', )),
     migrations.CreateModel(name='Tag', fields=[
      (
       'id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
      (
       'name', models.CharField(unique=True, max_length=200, verbose_name='name'))], options={'verbose_name_plural': 'tags', 
      'ordering': ('name', ), 
      'verbose_name': 'tag'}),
     migrations.AddField(model_name='articlelistplugin', name='tags', field=models.ManyToManyField(to='cmsplugin_articles_ai.Tag', related_name='article_list_plugins', verbose_name='tags')),
     migrations.AddField(model_name='article', name='tags', field=models.ManyToManyField(to='cmsplugin_articles_ai.Tag', related_name='articles', blank=True, verbose_name='tags'))]