# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ramusus/workspace/manufacture/env/src/django-odnoklassniki-photos/odnoklassniki_photos/migrations/0001_initial.py
# Compiled at: 2015-03-06 11:15:22
from __future__ import unicode_literals
from django.db import models, migrations
import m2m_history.fields

class Migration(migrations.Migration):
    dependencies = [
     ('contenttypes', '0001_initial'),
     ('odnoklassniki_users', '0001_initial')]
    operations = [
     migrations.CreateModel(name=b'Album', fields=[
      (
       b'fetched', models.DateTimeField(db_index=True, null=True, verbose_name=b'Обновлено', blank=True)),
      (
       b'id', models.BigIntegerField(help_text=b'Уникальный идентификатор', serialize=False, verbose_name=b'ID', primary_key=True)),
      (
       b'title', models.TextField()),
      (
       b'owner_name', models.TextField()),
      (
       b'owner_id', models.BigIntegerField(db_index=True)),
      (
       b'created', models.DateTimeField(null=True, db_index=True)),
      (
       b'updated', models.DateTimeField(null=True, db_index=True)),
      (
       b'photos_count', models.PositiveIntegerField(default=0)),
      (
       b'likes_count', models.PositiveIntegerField(default=0)),
      (
       b'last_like_date', models.DateTimeField(null=True)),
      (
       b'owner_content_type', models.ForeignKey(related_name=b'odnoklassniki_albums_owners', to=b'contenttypes.ContentType'))], options={b'verbose_name': b'Альбом фотографий Одноклассники', 
        b'verbose_name_plural': b'Альбомы фотографий Одноклассники'}, bases=(
      models.Model,)),
     migrations.CreateModel(name=b'Photo', fields=[
      (
       b'fetched', models.DateTimeField(db_index=True, null=True, verbose_name=b'Обновлено', blank=True)),
      (
       b'id', models.BigIntegerField(help_text=b'Уникальный идентификатор', serialize=False, verbose_name=b'ID', primary_key=True)),
      (
       b'created', models.DateTimeField(null=True)),
      (
       b'actions_count', models.PositiveIntegerField(default=0)),
      (
       b'comments_count', models.PositiveIntegerField(default=0)),
      (
       b'likes_count', models.PositiveIntegerField(default=0)),
      (
       b'last_like_date', models.DateTimeField(null=True)),
      (
       b'owner_id', models.BigIntegerField(db_index=True)),
      (
       b'owner_name', models.TextField()),
      (
       b'pic1024max', models.URLField(null=True)),
      (
       b'pic1024x768', models.URLField(null=True)),
      (
       b'pic128max', models.URLField(null=True)),
      (
       b'pic128x128', models.URLField(null=True)),
      (
       b'pic180min', models.URLField(null=True)),
      (
       b'pic190x190', models.URLField(null=True)),
      (
       b'pic240min', models.URLField(null=True)),
      (
       b'pic320min', models.URLField(null=True)),
      (
       b'pic50x50', models.URLField(null=True)),
      (
       b'pic640x480', models.URLField(null=True)),
      (
       b'standard_height', models.PositiveIntegerField(default=0)),
      (
       b'standard_width', models.PositiveIntegerField(default=0)),
      (
       b'text', models.TextField()),
      (
       b'album', models.ForeignKey(related_name=b'photos', to=b'odnoklassniki_photos.Album')),
      (
       b'like_users', m2m_history.fields.ManyToManyHistoryField(related_name=b'like_photos', to=b'odnoklassniki_users.User')),
      (
       b'owner_content_type', models.ForeignKey(related_name=b'odnoklassniki_photos_owners', to=b'contenttypes.ContentType'))], options={b'verbose_name': b'Фотография Одноклассники', 
        b'verbose_name_plural': b'Фотографии Одноклассники'}, bases=(
      models.Model,))]