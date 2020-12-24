# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ramusus/workspace/manufacture/env/src/django-vkontakte-polls/vkontakte_polls/migrations/0001_initial.py
# Compiled at: 2015-03-06 11:01:34
from __future__ import unicode_literals
from django.db import models, migrations

class Migration(migrations.Migration):
    dependencies = [
     ('vkontakte_users', '0001_initial'),
     ('vkontakte_wall', '0001_initial'),
     ('contenttypes', '0001_initial')]
    operations = [
     migrations.CreateModel(name=b'Answer', fields=[
      (
       b'fetched', models.DateTimeField(db_index=True, null=True, verbose_name=b'Обновлено', blank=True)),
      (
       b'remote_id', models.BigIntegerField(help_text=b'Уникальный идентификатор', serialize=False, verbose_name=b'ID', primary_key=True)),
      (
       b'text', models.TextField(verbose_name=b'Текст ответа')),
      (
       b'votes_count', models.PositiveIntegerField(help_text=b'Количество пользователей, проголосовавших за ответ', verbose_name=b'Голосов', db_index=True)),
      (
       b'rate', models.FloatField(help_text=b'Рейтинг ответа, в %', verbose_name=b'Рейтинг'))], options={b'verbose_name': b'Ответ опроса Вконтакте', 
        b'verbose_name_plural': b'Ответы опросов Вконтакте'}, bases=(
      models.Model,)),
     migrations.CreateModel(name=b'Poll', fields=[
      (
       b'fetched', models.DateTimeField(db_index=True, null=True, verbose_name=b'Обновлено', blank=True)),
      (
       b'remote_id', models.BigIntegerField(help_text=b'Уникальный идентификатор', serialize=False, verbose_name=b'ID', primary_key=True)),
      (
       b'owner_id', models.PositiveIntegerField(db_index=True)),
      (
       b'created', models.DateTimeField(verbose_name=b'Дата создания', db_index=True)),
      (
       b'question', models.TextField(verbose_name=b'Вопрос')),
      (
       b'votes_count', models.PositiveIntegerField(help_text=b'Общее количество ответивших пользователей', verbose_name=b'Голосов', db_index=True)),
      (
       b'answer_id', models.PositiveIntegerField(help_text=b'идентификатор ответа текущего пользователя', verbose_name=b'Ответ')),
      (
       b'owner_content_type', models.ForeignKey(related_name=b'vkontakte_polls_polls', to=b'contenttypes.ContentType')),
      (
       b'post', models.OneToOneField(related_name=b'poll', verbose_name=b'Сообщение, в котором опрос', to=b'vkontakte_wall.Post'))], options={b'verbose_name': b'Опрос Вконтакте', 
        b'verbose_name_plural': b'Опросы Вконтакте'}, bases=(
      models.Model,)),
     migrations.AddField(model_name=b'answer', name=b'poll', field=models.ForeignKey(related_name=b'answers', verbose_name=b'Опрос', to=b'vkontakte_polls.Poll'), preserve_default=True),
     migrations.AddField(model_name=b'answer', name=b'voters', field=models.ManyToManyField(related_name=b'poll_answers', verbose_name=b'Голосующие', to=b'vkontakte_users.User', blank=True), preserve_default=True)]