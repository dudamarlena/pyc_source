# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/huangwei/code/bee_apps_site/bee_django_social_feed/migrations/0001_initial.py
# Compiled at: 2018-05-22 22:00:09
from __future__ import unicode_literals
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    initial = True
    dependencies = [
     migrations.swappable_dependency(settings.AUTH_USER_MODEL)]
    operations = [
     migrations.CreateModel(name=b'Feed', fields=[
      (
       b'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name=b'ID')),
      (
       b'content', models.TextField(verbose_name=b'内容')),
      (
       b'created_at', models.DateTimeField(auto_now_add=True)),
      (
       b'publisher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name=b'发布者'))]),
     migrations.CreateModel(name=b'FeedComment', fields=[
      (
       b'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name=b'ID')),
      (
       b'comment', models.TextField(verbose_name=b'评论')),
      (
       b'feed', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=b'bee_django_social_feed.Feed')),
      (
       b'user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL))]),
     migrations.CreateModel(name=b'FeedEmoji', fields=[
      (
       b'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name=b'ID')),
      (
       b'emoji', models.IntegerField(default=0, verbose_name=b'感受')),
      (
       b'feed', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=b'bee_django_social_feed.Feed')),
      (
       b'user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL))])]