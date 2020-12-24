# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mmuth/PycharmProjects/djangocms-demo/demo/../github-plugins/djangocms-hubspot-blog/djangocms_hubspot_blog/migrations/0001_initial.py
# Compiled at: 2018-05-07 05:13:54
from __future__ import unicode_literals
from django.db import migrations, models
import djangocms_text_ckeditor.fields

class Migration(migrations.Migration):
    dependencies = []
    operations = [
     migrations.CreateModel(name=b'HubspotBlogAuthor', fields=[
      (
       b'hubspot_author_id', models.CharField(max_length=50, serialize=False, verbose_name=b'Hubspot Autor ID', primary_key=True)),
      (
       b'hubspot_user_id', models.CharField(max_length=50, verbose_name=b'Hubspot User ID')),
      (
       b'full_name', models.CharField(max_length=50, null=True, verbose_name=b'Name', blank=True)),
      (
       b'username', models.CharField(max_length=50, null=True, verbose_name=b'Benutzername', blank=True)),
      (
       b'email', models.EmailField(max_length=254, null=True, verbose_name=b'E-Mail', blank=True)),
      (
       b'facebook', models.URLField(null=True, verbose_name=b'Facebook', blank=True)),
      (
       b'linkedin', models.URLField(null=True, verbose_name=b'LinkedIn', blank=True)),
      (
       b'twitter', models.URLField(null=True, verbose_name=b'Twitter', blank=True)),
      (
       b'slug', models.CharField(max_length=200, null=True, verbose_name=b'Slug', blank=True)),
      (
       b'website', models.URLField(null=True, verbose_name=b'Website', blank=True))], options={b'ordering': ('full_name', ), 
        b'verbose_name': b'Blog Autor', 
        b'verbose_name_plural': b'Blog Autoren'}),
     migrations.CreateModel(name=b'HubspotBlogPost', fields=[
      (
       b'hubspot_post_id', models.BigIntegerField(serialize=False, verbose_name=b'Hubspot Post ID', primary_key=True)),
      (
       b'title', models.CharField(max_length=200, verbose_name=b'Titel')),
      (
       b'slug', models.CharField(max_length=200, verbose_name=b'Slug')),
      (
       b'excerpt', djangocms_text_ckeditor.fields.HTMLField(null=True, verbose_name=b'Ausschnitt', blank=True)),
      (
       b'content_html', djangocms_text_ckeditor.fields.HTMLField(null=True, verbose_name=b'Inhalt', blank=True)),
      (
       b'meta_description', models.CharField(max_length=500, null=True, verbose_name=b'Meta Description', blank=True)),
      (
       b'date_published', models.DateTimeField(null=True, verbose_name=b'Datum', blank=True)),
      (
       b'featured_image_url', models.URLField(null=True, verbose_name=b'Featured Image', blank=True)),
      (
       b'author', models.ForeignKey(verbose_name=b'Autor', blank=True, to=b'djangocms_hubspot_blog.HubspotBlogAuthor', null=True))], options={b'ordering': ('-date_published', ), 
        b'verbose_name': b'Blog Post', 
        b'verbose_name_plural': b'Blog Posts'}),
     migrations.CreateModel(name=b'HubspotBlogTopic', fields=[
      (
       b'id', models.CharField(max_length=50, serialize=False, verbose_name=b'ID', primary_key=True)),
      (
       b'name', models.CharField(max_length=50, null=True, verbose_name=b'Name', blank=True)),
      (
       b'description', models.CharField(max_length=200, null=True, verbose_name=b'Beschreibung', blank=True)),
      (
       b'slug', models.CharField(max_length=50, null=True, verbose_name=b'Slug', blank=True))], options={b'ordering': ('name', ), 
        b'verbose_name': b'Blog Topic', 
        b'verbose_name_plural': b'Blog Topics'}),
     migrations.AddField(model_name=b'hubspotblogpost', name=b'topics', field=models.ManyToManyField(to=b'djangocms_hubspot_blog.HubspotBlogTopic', verbose_name=b'Topics'))]