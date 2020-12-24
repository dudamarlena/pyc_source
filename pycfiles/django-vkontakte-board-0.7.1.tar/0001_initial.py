# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ramusus/workspace/manufacture/env/src/django-vkontakte-board/vkontakte_board/migrations/0001_initial.py
# Compiled at: 2015-03-06 11:00:19
from __future__ import unicode_literals
from django.db import models, migrations

class Migration(migrations.Migration):
    dependencies = [
     ('vkontakte_users', '0001_initial'),
     ('vkontakte_groups', '0001_initial')]
    operations = [
     migrations.CreateModel(name=b'Comment', fields=[
      (
       b'id', models.AutoField(verbose_name=b'ID', serialize=False, auto_created=True, primary_key=True)),
      (
       b'fetched', models.DateTimeField(db_index=True, null=True, verbose_name=b'Обновлено', blank=True)),
      (
       b'remote_id', models.CharField(help_text=b'Уникальный идентификатор', unique=True, max_length=b'50', verbose_name=b'ID')),
      (
       b'date', models.DateTimeField(help_text=b'Дата создания', db_index=True)),
      (
       b'text', models.TextField(verbose_name=b'Текст сообщения')),
      (
       b'author', models.ForeignKey(related_name=b'topics_comments', verbose_name=b'Aвтор комментария', to=b'vkontakte_users.User'))], options={b'verbose_name': b'Коммментарий дискуссии групп Вконтакте', 
        b'verbose_name_plural': b'Коммментарии дискуссий групп Вконтакте'}, bases=(
      models.Model,)),
     migrations.CreateModel(name=b'Topic', fields=[
      (
       b'id', models.AutoField(verbose_name=b'ID', serialize=False, auto_created=True, primary_key=True)),
      (
       b'fetched', models.DateTimeField(db_index=True, null=True, verbose_name=b'Обновлено', blank=True)),
      (
       b'remote_id', models.CharField(help_text=b'Уникальный идентификатор', unique=True, max_length=b'50', verbose_name=b'ID')),
      (
       b'title', models.CharField(max_length=500, verbose_name=b'Заголовок')),
      (
       b'created', models.DateTimeField(verbose_name=b'Дата создания', db_index=True)),
      (
       b'updated', models.DateTimeField(null=True, verbose_name=b'Дата последнего сообщения', db_index=True)),
      (
       b'is_closed', models.BooleanField(default=False, help_text=b'Тема является закрытой (в ней нельзя оставлять сообщения)', verbose_name=b'Закрыта?')),
      (
       b'is_fixed', models.BooleanField(default=False, help_text=b'Тема является прилепленной (находится в начале списка тем)', verbose_name=b'Прикреплена?')),
      (
       b'comments_count', models.PositiveIntegerField(default=0, verbose_name=b'Число сообщений в теме', db_index=True)),
      (
       b'first_comment', models.TextField(verbose_name=b'Текст первого сообщения')),
      (
       b'last_comment', models.TextField(verbose_name=b'Текст последнего сообщения')),
      (
       b'created_by', models.ForeignKey(related_name=b'topics_created', verbose_name=b'Пользователь, создавший тему', to=b'vkontakte_users.User')),
      (
       b'group', models.ForeignKey(related_name=b'topics', verbose_name=b'Группа', to=b'vkontakte_groups.Group')),
      (
       b'updated_by', models.ForeignKey(related_name=b'topics_updated', verbose_name=b'Пользователь, оставивший последнее сообщение', to=b'vkontakte_users.User'))], options={b'verbose_name': b'Дискуссия групп Вконтакте', 
        b'verbose_name_plural': b'Дискуссии групп Вконтакте'}, bases=(
      models.Model,)),
     migrations.AddField(model_name=b'comment', name=b'topic', field=models.ForeignKey(related_name=b'comments', verbose_name=b'Тема', to=b'vkontakte_board.Topic'), preserve_default=True)]