# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: G:\python\hhwork\extra_apps\xadmin\migrations\0001_initial.py
# Compiled at: 2018-12-16 22:27:14
from __future__ import unicode_literals
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    initial = True
    dependencies = [
     migrations.swappable_dependency(settings.AUTH_USER_MODEL)]
    operations = [
     migrations.CreateModel(name=b'Bookmark', fields=[
      (
       b'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name=b'ID')),
      (
       b'title', models.CharField(max_length=128, verbose_name=b'Title')),
      (
       b'url_name', models.CharField(max_length=64, verbose_name=b'Url Name')),
      (
       b'query', models.CharField(blank=True, max_length=1000, verbose_name=b'Query String')),
      (
       b'is_share', models.BooleanField(default=False, verbose_name=b'Is Shared')),
      (
       b'content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=b'contenttypes.ContentType')),
      (
       b'user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name=b'user'))], options={b'verbose_name': b'Bookmark', 
        b'verbose_name_plural': b'Bookmarks'}),
     migrations.CreateModel(name=b'UserSettings', fields=[
      (
       b'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name=b'ID')),
      (
       b'key', models.CharField(max_length=256, verbose_name=b'Settings Key')),
      (
       b'value', models.TextField(verbose_name=b'Settings Content')),
      (
       b'user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name=b'user'))], options={b'verbose_name': b'User Setting', 
        b'verbose_name_plural': b'User Settings'}),
     migrations.CreateModel(name=b'UserWidget', fields=[
      (
       b'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name=b'ID')),
      (
       b'page_id', models.CharField(max_length=256, verbose_name=b'Page')),
      (
       b'widget_type', models.CharField(max_length=50, verbose_name=b'Widget Type')),
      (
       b'value', models.TextField(verbose_name=b'Widget Params')),
      (
       b'user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name=b'user'))], options={b'verbose_name': b'User Widget', 
        b'verbose_name_plural': b'User Widgets'})]