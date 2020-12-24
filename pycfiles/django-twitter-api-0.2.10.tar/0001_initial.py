# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ramusus/workspace/manufacture/env/src/django-twitter-api/twitter_api/migrations/0001_initial.py
# Compiled at: 2015-12-19 16:33:42
from __future__ import unicode_literals
from django.db import models, migrations
import m2m_history.fields, annoying.fields

class Migration(migrations.Migration):
    dependencies = []
    operations = [
     migrations.CreateModel(name=b'Status', fields=[
      (
       b'id', models.BigIntegerField(serialize=False, primary_key=True)),
      (
       b'created_at', models.DateTimeField()),
      (
       b'lang', models.CharField(max_length=10)),
      (
       b'entities', annoying.fields.JSONField()),
      (
       b'fetched', models.DateTimeField(null=True, verbose_name=b'Fetched', blank=True)),
      (
       b'text', models.TextField()),
      (
       b'favorited', models.BooleanField(default=False)),
      (
       b'retweeted', models.BooleanField(default=False)),
      (
       b'truncated', models.BooleanField(default=False)),
      (
       b'source', models.CharField(max_length=100)),
      (
       b'source_url', models.URLField(null=True)),
      (
       b'favorites_count', models.PositiveIntegerField()),
      (
       b'retweets_count', models.PositiveIntegerField()),
      (
       b'replies_count', models.PositiveIntegerField(null=True)),
      (
       b'place', annoying.fields.JSONField(null=True)),
      (
       b'contributors', annoying.fields.JSONField(null=True)),
      (
       b'coordinates', annoying.fields.JSONField(null=True)),
      (
       b'geo', annoying.fields.JSONField(null=True))], options={b'abstract': False}, bases=(
      models.Model,)),
     migrations.CreateModel(name=b'User', fields=[
      (
       b'id', models.BigIntegerField(serialize=False, primary_key=True)),
      (
       b'created_at', models.DateTimeField()),
      (
       b'lang', models.CharField(max_length=10)),
      (
       b'entities', annoying.fields.JSONField()),
      (
       b'fetched', models.DateTimeField(null=True, verbose_name=b'Fetched', blank=True)),
      (
       b'screen_name', models.CharField(unique=True, max_length=50, verbose_name=b'Screen name')),
      (
       b'name', models.CharField(max_length=100, verbose_name=b'Name')),
      (
       b'description', models.TextField(verbose_name=b'Description')),
      (
       b'location', models.CharField(max_length=100, verbose_name=b'Location')),
      (
       b'time_zone', models.CharField(max_length=100, null=True, verbose_name=b'Time zone')),
      (
       b'contributors_enabled', models.BooleanField(default=False, verbose_name=b'Contributors enabled')),
      (
       b'default_profile', models.BooleanField(default=False, verbose_name=b'Default profile')),
      (
       b'default_profile_image', models.BooleanField(default=False, verbose_name=b'Default profile image')),
      (
       b'follow_request_sent', models.BooleanField(default=False, verbose_name=b'Follow request sent')),
      (
       b'following', models.BooleanField(default=False, verbose_name=b'Following')),
      (
       b'geo_enabled', models.BooleanField(default=False, verbose_name=b'Geo enabled')),
      (
       b'is_translator', models.BooleanField(default=False, verbose_name=b'Is translator')),
      (
       b'notifications', models.BooleanField(default=False, verbose_name=b'Notifications')),
      (
       b'profile_use_background_image', models.BooleanField(default=False, verbose_name=b'Profile use background image')),
      (
       b'protected', models.BooleanField(default=False, verbose_name=b'Protected')),
      (
       b'verified', models.BooleanField(default=False, verbose_name=b'Verified')),
      (
       b'profile_background_image_url', models.URLField(max_length=300, null=True)),
      (
       b'profile_background_image_url_https', models.URLField(max_length=300, null=True)),
      (
       b'profile_background_tile', models.BooleanField(default=False)),
      (
       b'profile_background_color', models.CharField(max_length=6)),
      (
       b'profile_banner_url', models.URLField(max_length=300, null=True)),
      (
       b'profile_image_url', models.URLField(max_length=300, null=True)),
      (
       b'profile_image_url_https', models.URLField(max_length=300)),
      (
       b'url', models.URLField(max_length=300, null=True)),
      (
       b'profile_link_color', models.CharField(max_length=6)),
      (
       b'profile_sidebar_border_color', models.CharField(max_length=6)),
      (
       b'profile_sidebar_fill_color', models.CharField(max_length=6)),
      (
       b'profile_text_color', models.CharField(max_length=6)),
      (
       b'favorites_count', models.PositiveIntegerField()),
      (
       b'followers_count', models.PositiveIntegerField()),
      (
       b'friends_count', models.PositiveIntegerField()),
      (
       b'listed_count', models.PositiveIntegerField()),
      (
       b'statuses_count', models.PositiveIntegerField()),
      (
       b'utc_offset', models.IntegerField(null=True)),
      (
       b'followers', m2m_history.fields.ManyToManyHistoryField(to=b'twitter_api.User'))], options={b'abstract': False}, bases=(
      models.Model,)),
     migrations.AddField(model_name=b'status', name=b'author', field=models.ForeignKey(related_name=b'statuses', to=b'twitter_api.User'), preserve_default=True),
     migrations.AddField(model_name=b'status', name=b'favorites_users', field=m2m_history.fields.ManyToManyHistoryField(related_name=b'favorites', to=b'twitter_api.User'), preserve_default=True),
     migrations.AddField(model_name=b'status', name=b'in_reply_to_status', field=models.ForeignKey(related_name=b'replies', to=b'twitter_api.Status', null=True), preserve_default=True),
     migrations.AddField(model_name=b'status', name=b'in_reply_to_user', field=models.ForeignKey(related_name=b'replies', to=b'twitter_api.User', null=True), preserve_default=True),
     migrations.AddField(model_name=b'status', name=b'retweeted_status', field=models.ForeignKey(related_name=b'retweets', to=b'twitter_api.Status', null=True), preserve_default=True)]