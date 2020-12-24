# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/eliotberriot/Seafile/kii/kii_main/kii/stream/migrations/0004_auto_20141217_1222.py
# Compiled at: 2015-01-17 16:40:50
# Size of source mod 2**32: 1930 bytes
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
     migrations.CreateModel(name='ItemComment', fields=[
      (
       'id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
      (
       'content', kii.base_models.fields.MarkdownField()),
      (
       'content_markup_type', models.CharField(default='markdown', max_length=255)),
      (
       '_content_rendered', models.TextField(default='')),
      (
       'published', models.BooleanField(default=False)),
      (
       'junk', models.NullBooleanField(default=None)),
      (
       'subject', models.ForeignKey(related_name='comments', to='stream.StreamItem')),
      (
       'user', models.ForeignKey(related_name='itemcomments', default=None, blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
      (
       'user_profile', models.ForeignKey(default=None, blank=True, to='discussion.AnonymousCommenterProfile', null=True))], options={'abstract': False}, bases=(
      models.Model,)),
     migrations.RemoveField(model_name='streamitemcomment', name='subject'),
     migrations.RemoveField(model_name='streamitemcomment', name='user'),
     migrations.RemoveField(model_name='streamitemcomment', name='user_profile'),
     migrations.DeleteModel(name='StreamItemComment')]