# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ramusus/workspace/manufacture/env/src/django-vkontakte-groups/vkontakte_groups/migrations/0001_initial.py
# Compiled at: 2015-03-06 10:50:42
from __future__ import unicode_literals
from django.db import models, migrations
import m2m_history.fields, vkontakte_api.models

class Migration(migrations.Migration):
    dependencies = [
     ('vkontakte_users', '0001_initial')]
    operations = [
     migrations.CreateModel(name=b'Group', fields=[
      (
       b'fetched', models.DateTimeField(db_index=True, null=True, verbose_name=b'Обновлено', blank=True)),
      (
       b'remote_id', models.BigIntegerField(help_text=b'Уникальный идентификатор', serialize=False, verbose_name=b'ID', primary_key=True)),
      (
       b'name', models.CharField(max_length=800)),
      (
       b'screen_name', models.CharField(max_length=50, verbose_name=b'Короткое имя группы', db_index=True)),
      (
       b'is_closed', models.NullBooleanField(verbose_name=b'Флаг закрытой группы')),
      (
       b'is_admin', models.NullBooleanField(verbose_name=b'Пользователь является администратором')),
      (
       b'members_count', models.IntegerField(null=True, verbose_name=b'Всего участников')),
      (
       b'verified', models.NullBooleanField(verbose_name=b'Флаг официальной группы')),
      (
       b'type', models.CharField(max_length=10, verbose_name=b'Тип объекта', choices=[('group', 'Группа'), ('page', 'Страница'), ('event', 'Событие')])),
      (
       b'photo', models.URLField()),
      (
       b'photo_big', models.URLField()),
      (
       b'photo_medium', models.URLField()),
      (
       b'members', m2m_history.fields.ManyToManyHistoryField(related_name=b'members_groups', to=b'vkontakte_users.User')),
      (
       b'users', models.ManyToManyField(to=b'vkontakte_users.User'))], options={b'verbose_name': b'Vkontakte group', 
        b'verbose_name_plural': b'Vkontakte groups'}, bases=(
      vkontakte_api.models.RemoteIdModelMixin, models.Model))]