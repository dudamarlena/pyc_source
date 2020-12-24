# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ramusus/workspace/manufacture/env/src/django-instagram-api/instagram_api/migrations/0001_initial.py
# Compiled at: 2015-12-21 18:12:34
from __future__ import unicode_literals
from django.db import models, migrations
import m2m_history.fields

class Migration(migrations.Migration):
    dependencies = []
    operations = [
     migrations.CreateModel(name=b'Comment', fields=[
      (
       b'fetched', models.DateTimeField(null=True, verbose_name=b'Fetched', blank=True)),
      (
       b'id', models.BigIntegerField(serialize=False, primary_key=True)),
      (
       b'text', models.TextField()),
      (
       b'created_time', models.DateTimeField())], options={b'abstract': False}, bases=(
      models.Model,)),
     migrations.CreateModel(name=b'Media', fields=[
      (
       b'id', models.AutoField(verbose_name=b'ID', serialize=False, auto_created=True, primary_key=True)),
      (
       b'fetched', models.DateTimeField(null=True, verbose_name=b'Fetched', blank=True)),
      (
       b'remote_id', models.CharField(unique=True, max_length=100)),
      (
       b'caption', models.TextField(blank=True)),
      (
       b'link', models.URLField(max_length=300)),
      (
       b'type', models.CharField(max_length=20)),
      (
       b'image_low_resolution', models.URLField()),
      (
       b'image_standard_resolution', models.URLField()),
      (
       b'image_thumbnail', models.URLField()),
      (
       b'video_low_bandwidth', models.URLField()),
      (
       b'video_low_resolution', models.URLField()),
      (
       b'video_standard_resolution', models.URLField()),
      (
       b'created_time', models.DateTimeField()),
      (
       b'comments_count', models.PositiveIntegerField(null=True)),
      (
       b'likes_count', models.PositiveIntegerField(null=True))], options={b'abstract': False}, bases=(
      models.Model,)),
     migrations.CreateModel(name=b'Tag', fields=[
      (
       b'id', models.AutoField(verbose_name=b'ID', serialize=False, auto_created=True, primary_key=True)),
      (
       b'fetched', models.DateTimeField(null=True, verbose_name=b'Fetched', blank=True)),
      (
       b'name', models.CharField(unique=True, max_length=29)),
      (
       b'media_count', models.PositiveIntegerField(null=True)),
      (
       b'media_feed', models.ManyToManyField(related_name=b'tags', to=b'instagram_api.Media'))], options={b'abstract': False}, bases=(
      models.Model,)),
     migrations.CreateModel(name=b'User', fields=[
      (
       b'fetched', models.DateTimeField(null=True, verbose_name=b'Fetched', blank=True)),
      (
       b'id', models.BigIntegerField(serialize=False, primary_key=True)),
      (
       b'username', models.CharField(unique=True, max_length=50)),
      (
       b'full_name', models.CharField(max_length=255)),
      (
       b'bio', models.CharField(max_length=255, verbose_name=b'BIO')),
      (
       b'profile_picture', models.URLField(max_length=300)),
      (
       b'website', models.URLField(max_length=300)),
      (
       b'followers_count', models.PositiveIntegerField(null=True)),
      (
       b'media_count', models.PositiveIntegerField(null=True)),
      (
       b'followers', m2m_history.fields.ManyToManyHistoryField(to=b'instagram_api.User'))], options={b'abstract': False}, bases=(
      models.Model,)),
     migrations.AddField(model_name=b'media', name=b'likes_users', field=m2m_history.fields.ManyToManyHistoryField(related_name=b'likes_media', to=b'instagram_api.User'), preserve_default=True),
     migrations.AddField(model_name=b'media', name=b'user', field=models.ForeignKey(related_name=b'media_feed', to=b'instagram_api.User'), preserve_default=True),
     migrations.AddField(model_name=b'comment', name=b'media', field=models.ForeignKey(related_name=b'comments', to=b'instagram_api.Media'), preserve_default=True),
     migrations.AddField(model_name=b'comment', name=b'owner', field=models.ForeignKey(related_name=b'media_comments', to=b'instagram_api.User'), preserve_default=True),
     migrations.AddField(model_name=b'comment', name=b'user', field=models.ForeignKey(related_name=b'comments', to=b'instagram_api.User'), preserve_default=True)]