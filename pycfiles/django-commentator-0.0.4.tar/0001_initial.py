# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/smidth/GitHub/django-commentator/commentator/migrations/0001_initial.py
# Compiled at: 2015-03-18 05:49:53
from __future__ import unicode_literals
from django.db import models, migrations
from django.conf import settings

class Migration(migrations.Migration):
    dependencies = [
     migrations.swappable_dependency(settings.AUTH_USER_MODEL),
     ('contenttypes', '0001_initial')]
    operations = [
     migrations.CreateModel(name=b'Comment', fields=[
      (
       b'id',
       models.AutoField(verbose_name=b'ID', serialize=False, auto_created=True, primary_key=True)),
      (
       b'text',
       models.TextField(null=True, verbose_name=b'Comment', blank=True)),
      (
       b'raw', models.TextField(verbose_name=b'Raw content')),
      (
       b'edited',
       models.BooleanField(default=False, verbose_name=b'Edited')),
      (
       b'deleted',
       models.BooleanField(default=False, verbose_name=b'Deleted')),
      (
       b'created_at', models.DateTimeField(auto_now_add=True)),
      (
       b'updated_at', models.DateTimeField(auto_now=True)),
      (
       b'deleted_at', models.DateTimeField(null=True, blank=True)),
      (
       b'path',
       models.CharField(default=b'', max_length=255, blank=True)),
      (
       b'author',
       models.ForeignKey(verbose_name=b'User', to=settings.AUTH_USER_MODEL)),
      (
       b'part_of',
       models.ForeignKey(default=None, blank=True, to=b'commentator.Comment', null=True, verbose_name=b'Parent'))], options={b'ordering': ('thread', 'created_at'), 
        b'db_table': b'commentaror_comments', 
        b'verbose_name': b'Comment', 
        b'verbose_name_plural': b'Comments'}, bases=(
      models.Model,)),
     migrations.CreateModel(name=b'Thread', fields=[
      (
       b'id',
       models.AutoField(verbose_name=b'ID', serialize=False, auto_created=True, primary_key=True)),
      (
       b'object_pk', models.TextField(verbose_name=b'object ID')),
      (
       b'last_message',
       models.DateTimeField(db_index=True, null=True, blank=True)),
      (
       b'created_at', models.DateTimeField(auto_now_add=True)),
      (
       b'updated_at', models.DateTimeField(auto_now=True)),
      (
       b'content_type',
       models.ForeignKey(related_name=b'content_type_set_for_thread', verbose_name=b'content type', to=b'contenttypes.ContentType'))], options={b'ordering': ('-last_message', ), 
        b'db_table': b'commentaror_threads', 
        b'verbose_name': b'Thread', 
        b'verbose_name_plural': b'Threads'}, bases=(
      models.Model,)),
     migrations.AddField(model_name=b'comment', name=b'thread', field=models.ForeignKey(verbose_name=b'Thread', to=b'commentator.Thread'), preserve_default=True)]