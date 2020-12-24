# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/bfschott/Source/cmsplugin-newsplus/cmsplugin_newsplus/migrations/0001_initial.py
# Compiled at: 2016-06-07 17:28:14
from __future__ import unicode_literals
from django.db import models, migrations
import datetime
from django.utils.timezone import utc

class Migration(migrations.Migration):
    dependencies = [
     ('cms', '__first__')]
    operations = [
     migrations.CreateModel(name=b'LatestNewsPlugin', fields=[
      (
       b'cmsplugin_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to=b'cms.CMSPlugin')),
      (
       b'limit', models.PositiveIntegerField(help_text=b'Limits the number of items that will be displayed', verbose_name=b'Number of news items to show'))], options={b'abstract': False}, bases=('cms.cmsplugin', )),
     migrations.CreateModel(name=b'News', fields=[
      (
       b'id', models.AutoField(verbose_name=b'ID', serialize=False, auto_created=True, primary_key=True)),
      (
       b'title', models.CharField(max_length=255, verbose_name=b'Title')),
      (
       b'slug', models.SlugField(help_text=b'A slug is a short name which uniquely identifies the news item for this day', verbose_name=b'Slug', unique_for_date=b'pub_date')),
      (
       b'excerpt', models.TextField(verbose_name=b'Excerpt', blank=True)),
      (
       b'content', models.TextField(verbose_name=b'Content', blank=True)),
      (
       b'is_published', models.BooleanField(default=False, verbose_name=b'Published')),
      (
       b'pub_date', models.DateTimeField(default=datetime.datetime(2015, 2, 9, 16, 52, 1, 765997, tzinfo=utc), verbose_name=b'Publication date')),
      (
       b'created', models.DateTimeField(auto_now_add=True)),
      (
       b'updated', models.DateTimeField(auto_now=True)),
      (
       b'link', models.URLField(help_text=b'This link will be used a absolute url for this item and replaces the view logic. <br />Note that by default this only applies for items with  an empty "content" field.', null=True, verbose_name=b'Link', blank=True))], options={b'ordering': ('-pub_date', ), 
        b'verbose_name': b'News', 
        b'verbose_name_plural': b'News'}, bases=(
      models.Model,)),
     migrations.CreateModel(name=b'NewsImage', fields=[
      (
       b'id', models.AutoField(verbose_name=b'ID', serialize=False, auto_created=True, primary_key=True)),
      (
       b'image', models.ImageField(upload_to=b'news_images')),
      (
       b'news', models.ForeignKey(related_name=b'images', to=b'cmsplugin_newsplus.News'))], options={}, bases=(
      models.Model,))]