# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/eliotberriot/Seafile/kii/kii_main/kii/stream/migrations/0004_auto_20141217_1222.py
# Compiled at: 2015-01-17 16:40:50
from __future__ import unicode_literals
from django.db import models, migrations
import kii.base_models.fields
from django.conf import settings

class Migration(migrations.Migration):
    dependencies = [
     migrations.swappable_dependency(settings.AUTH_USER_MODEL),
     ('discussion', '0001_initial'),
     ('stream', '0003_auto_20141216_1441')]
    operations = [
     migrations.CreateModel(name=b'ItemComment', fields=[
      (
       b'id', models.AutoField(verbose_name=b'ID', serialize=False, auto_created=True, primary_key=True)),
      (
       b'content', kii.base_models.fields.MarkdownField()),
      (
       b'content_markup_type', models.CharField(default=b'markdown', max_length=255)),
      (
       b'_content_rendered', models.TextField(default=b'')),
      (
       b'published', models.BooleanField(default=False)),
      (
       b'junk', models.NullBooleanField(default=None)),
      (
       b'subject', models.ForeignKey(related_name=b'comments', to=b'stream.StreamItem')),
      (
       b'user', models.ForeignKey(related_name=b'itemcomments', default=None, blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
      (
       b'user_profile', models.ForeignKey(default=None, blank=True, to=b'discussion.AnonymousCommenterProfile', null=True))], options={b'abstract': False}, bases=(
      models.Model,)),
     migrations.RemoveField(model_name=b'streamitemcomment', name=b'subject'),
     migrations.RemoveField(model_name=b'streamitemcomment', name=b'user'),
     migrations.RemoveField(model_name=b'streamitemcomment', name=b'user_profile'),
     migrations.DeleteModel(name=b'StreamItemComment')]