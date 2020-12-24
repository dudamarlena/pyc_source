# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ramusus/workspace/manufacture/env/src/django-vkontakte-users/vkontakte_users/migrations/0001_initial.py
# Compiled at: 2016-02-12 18:37:36
from __future__ import unicode_literals
from django.db import models, migrations
import django.db.models.deletion, vkontakte_api.models

class Migration(migrations.Migration):
    dependencies = [
     ('vkontakte_places', '__first__')]
    operations = [
     migrations.CreateModel(name=b'User', fields=[
      (
       b'fetched', models.DateTimeField(db_index=True, null=True, verbose_name=b'Обновлено', blank=True)),
      (
       b'remote_id', models.BigIntegerField(help_text=b'Уникальный идентификатор', serialize=False, verbose_name=b'ID', primary_key=True)),
      (
       b'first_name', models.CharField(max_length=200)),
      (
       b'last_name', models.CharField(max_length=200)),
      (
       b'screen_name', models.CharField(max_length=100, db_index=True)),
      (
       b'sex', models.PositiveSmallIntegerField(db_index=True, null=True, choices=[(0, 'не ук.'), (1, 'жен.'), (2, 'муж.')])),
      (
       b'age', models.PositiveSmallIntegerField(null=True, db_index=True)),
      (
       b'timezone', models.IntegerField(null=True)),
      (
       b'rate', models.PositiveIntegerField(null=True, db_index=True)),
      (
       b'bdate', models.CharField(max_length=100)),
      (
       b'activity', models.TextField()),
      (
       b'relation', models.SmallIntegerField(db_index=True, null=True, choices=[(1, 'Не женат / замужем'), (2, 'Есть друг / подруга'), (3, 'Помолвлен / помолвлена'), (4, 'Женат / замужем'), (5, 'Всё сложно'), (6, 'В активном поиске'), (7, 'Влюблён / влюблена')])),
      (
       b'wall_comments', models.NullBooleanField()),
      (
       b'graduation', models.PositiveIntegerField(null=True, verbose_name=b'Дата окончания вуза')),
      (
       b'university', models.PositiveIntegerField(null=True)),
      (
       b'university_name', models.CharField(max_length=500)),
      (
       b'faculty', models.PositiveIntegerField(null=True)),
      (
       b'faculty_name', models.CharField(max_length=500)),
      (
       b'has_mobile', models.NullBooleanField(db_index=True)),
      (
       b'home_phone', models.CharField(max_length=50)),
      (
       b'mobile_phone', models.CharField(max_length=50)),
      (
       b'photo', models.URLField()),
      (
       b'photo_big', models.URLField()),
      (
       b'photo_medium', models.URLField()),
      (
       b'photo_medium_rec', models.URLField()),
      (
       b'photo_rec', models.URLField()),
      (
       b'twitter', models.CharField(max_length=500)),
      (
       b'facebook', models.CharField(max_length=500)),
      (
       b'facebook_name', models.CharField(max_length=500)),
      (
       b'skype', models.CharField(max_length=500)),
      (
       b'livejournal', models.CharField(max_length=500)),
      (
       b'interests', models.TextField()),
      (
       b'movies', models.TextField()),
      (
       b'tv', models.TextField()),
      (
       b'books', models.TextField()),
      (
       b'games', models.TextField()),
      (
       b'about', models.TextField()),
      (
       b'friends_count', models.PositiveIntegerField(default=0, verbose_name=b'Друзей')),
      (
       b'counters_updated', models.DateTimeField(help_text=b'Счетчики были обновлены', null=True, db_index=True)),
      (
       b'sum_counters', models.PositiveIntegerField(default=0, help_text=b'Сумма всех счетчиков')),
      (
       b'albums', models.PositiveIntegerField(default=0, verbose_name=b'Фотоальбомов')),
      (
       b'videos', models.PositiveIntegerField(default=0, verbose_name=b'Видеозаписей')),
      (
       b'audios', models.PositiveIntegerField(default=0, verbose_name=b'Аудиозаписей')),
      (
       b'followers', models.PositiveIntegerField(default=0, verbose_name=b'Подписчиков')),
      (
       b'friends', models.PositiveIntegerField(default=0, verbose_name=b'Друзей', db_index=True)),
      (
       b'mutual_friends', models.PositiveIntegerField(default=0, verbose_name=b'Общих друзей')),
      (
       b'notes', models.PositiveIntegerField(default=0, verbose_name=b'Заметок')),
      (
       b'subscriptions', models.PositiveIntegerField(default=0, verbose_name=b'Подписок (только пользователи)')),
      (
       b'user_photos', models.PositiveIntegerField(default=0, verbose_name=b'Фотографий с пользователем')),
      (
       b'user_videos', models.PositiveIntegerField(default=0, verbose_name=b'Видеозаписей с пользователем')),
      (
       b'is_deactivated', models.BooleanField(default=False, db_index=True, verbose_name=b'Деактивирован?')),
      (
       b'has_avatar', models.BooleanField(default=True, db_index=True, verbose_name=b'Есть аватар?')),
      (
       b'city', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, to=b'vkontakte_places.City', null=True)),
      (
       b'country', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, to=b'vkontakte_places.Country', null=True)),
      (
       b'friends_users', models.ManyToManyField(related_name=b'followers_users', to=b'vkontakte_users.User'))], options={b'verbose_name': b'Пользователь Вконтакте', 
        b'verbose_name_plural': b'Пользователи Вконтакте'}, bases=(
      vkontakte_api.models.RemoteIdModelMixin, models.Model)),
     migrations.CreateModel(name=b'UserRelative', fields=[
      (
       b'id', models.AutoField(verbose_name=b'ID', serialize=False, auto_created=True, primary_key=True)),
      (
       b'type', models.CharField(max_length=20, verbose_name=b'Тип родственной связи', choices=[('grandchild', 'внук/внучка'), ('grandparent', 'дедушка/бабушка'), ('child', 'сын/дочка'), ('sibling', 'брат/сестра'), ('parent', 'мама/папа')])),
      (
       b'user1', models.ForeignKey(related_name=b'user_relatives1', to=b'vkontakte_users.User')),
      (
       b'user2', models.ForeignKey(related_name=b'user_relatives2', to=b'vkontakte_users.User'))], options={}, bases=(
      models.Model,))]