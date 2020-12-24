# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ramusus/workspace/manufacture/env/src/django-facebook-posts/facebook_posts/migrations/0001_initial.py
# Compiled at: 2015-03-06 11:03:12
from __future__ import unicode_literals
from django.db import models, migrations
import m2m_history.fields, annoying.fields

class Migration(migrations.Migration):
    dependencies = [
     ('facebook_users', '__first__'),
     ('contenttypes', '0001_initial'),
     ('facebook_applications', '__first__')]
    operations = [
     migrations.CreateModel(name=b'Post', fields=[
      (
       b'id', models.AutoField(verbose_name=b'ID', serialize=False, auto_created=True, primary_key=True)),
      (
       b'graph_id', models.CharField(help_text=b'Unique graph ID', unique=True, max_length=70, verbose_name=b'ID')),
      (
       b'author_json', annoying.fields.JSONField(help_text=b'Information about the user who posted the message', null=True)),
      (
       b'author_id', models.BigIntegerField(null=True, db_index=True)),
      (
       b'likes_count', models.PositiveIntegerField(help_text=b'The number of likes of this item', null=True)),
      (
       b'shares_count', models.PositiveIntegerField(help_text=b'The number of shares of this item', null=True)),
      (
       b'comments_count', models.PositiveIntegerField(help_text=b'The number of comments of this item', null=True)),
      (
       b'owners_json', annoying.fields.JSONField(help_text=b'Profiles mentioned or targeted in this post', null=True)),
      (
       b'message', models.TextField(help_text=b'The message')),
      (
       b'object_id', models.BigIntegerField(help_text=b'The Facebook object id for an uploaded photo or video', null=True)),
      (
       b'created_time', models.DateTimeField(help_text=b'The time the post was initially published', db_index=True)),
      (
       b'updated_time', models.DateTimeField(help_text=b'The time of the last comment on this post', null=True)),
      (
       b'picture', models.TextField(help_text=b'If available, a link to the picture included with this post')),
      (
       b'source', models.TextField(help_text=b'A URL to a Flash movie or video file to be embedded within the post')),
      (
       b'link', models.URLField(help_text=b'The link attached to this post', max_length=1000)),
      (
       b'icon', models.URLField(help_text=b'A link to an icon representing the type of this post', max_length=500)),
      (
       b'name', models.TextField(help_text=b'The name of the link')),
      (
       b'type', models.CharField(help_text=b'A string indicating the type for this post (including link, photo, video)', max_length=10, db_index=True)),
      (
       b'caption', models.TextField(help_text=b'The caption of the link (appears beneath the link name)')),
      (
       b'description', models.TextField(help_text=b'A description of the link (appears beneath the link caption)')),
      (
       b'story', models.TextField(help_text=b'Text of stories not intentionally generatd by users, such as those generated when two users become friends; you must have the "Include recent activity stories" migration enabled in your app to retrieve these stories')),
      (
       b'properties', annoying.fields.JSONField(help_text=b'A list of properties for an uploaded video, for example, the length of the video', null=True)),
      (
       b'actions', annoying.fields.JSONField(help_text=b'A list of available actions on the post (including commenting, liking, and an optional app-specified action)', null=True)),
      (
       b'privacy', annoying.fields.JSONField(help_text=b'The privacy settings of the Post', null=True)),
      (
       b'place', annoying.fields.JSONField(help_text=b'Location associated with a Post, if any', null=True)),
      (
       b'message_tags', annoying.fields.JSONField(help_text=b'Objects tagged in the message (Users, Pages, etc)', null=True)),
      (
       b'story_tags', annoying.fields.JSONField(help_text=b'Objects (Users, Pages, etc) tagged in a non-intentional story; you must have the "Include recent activity stories" migration enabled in your app to retrieve these tags', null=True)),
      (
       b'with_tags', annoying.fields.JSONField(help_text=b'Objects (Users, Pages, etc) tagged as being with the publisher of the post ("Who are you with?" on Facebook)', null=True)),
      (
       b'likes_json', annoying.fields.JSONField(help_text=b'Likes for this post', null=True)),
      (
       b'comments_json', annoying.fields.JSONField(help_text=b'Comments for this post', null=True)),
      (
       b'shares_json', annoying.fields.JSONField(help_text=b'Shares for this post', null=True)),
      (
       b'status_type', models.CharField(max_length=100)),
      (
       b'expanded_height', models.IntegerField(null=True)),
      (
       b'expanded_width', models.IntegerField(null=True)),
      (
       b'application', models.ForeignKey(related_name=b'posts', to=b'facebook_applications.Application', help_text=b'Application this post came from', null=True)),
      (
       b'author_content_type', models.ForeignKey(related_name=b'content_type_authors_facebook_posts_posts', to=b'contenttypes.ContentType', null=True)),
      (
       b'likes_users', m2m_history.fields.ManyToManyHistoryField(related_name=b'like_posts', to=b'facebook_users.User')),
      (
       b'shares_users', m2m_history.fields.ManyToManyHistoryField(related_name=b'shares_posts', to=b'facebook_users.User'))], options={b'verbose_name': b'Facebook post', 
        b'verbose_name_plural': b'Facebook posts'}, bases=(
      models.Model,)),
     migrations.CreateModel(name=b'PostOwner', fields=[
      (
       b'id', models.AutoField(verbose_name=b'ID', serialize=False, auto_created=True, primary_key=True)),
      (
       b'owner_id', models.PositiveIntegerField(null=True, db_index=True)),
      (
       b'owner_content_type', models.ForeignKey(related_name=b'facebook_page_posts', to=b'contenttypes.ContentType', null=True)),
      (
       b'post', models.ForeignKey(related_name=b'owners', to=b'facebook_posts.Post'))], options={}, bases=(
      models.Model,)),
     migrations.AlterUniqueTogether(name=b'postowner', unique_together=set([('post', 'owner_content_type', 'owner_id')]))]