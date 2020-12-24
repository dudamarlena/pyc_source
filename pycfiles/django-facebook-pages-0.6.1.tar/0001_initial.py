# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ramusus/workspace/manufacture/env/src/django-facebook-pages/facebook_pages/migrations/0001_initial.py
# Compiled at: 2015-03-06 11:12:50
from __future__ import unicode_literals
from django.db import models, migrations
import annoying.fields

class Migration(migrations.Migration):
    dependencies = []
    operations = [
     migrations.CreateModel(name=b'Page', fields=[
      (
       b'id', models.AutoField(verbose_name=b'ID', serialize=False, auto_created=True, primary_key=True)),
      (
       b'graph_id', models.CharField(help_text=b'Unique graph ID', unique=True, max_length=70, verbose_name=b'ID')),
      (
       b'name', models.CharField(help_text=b"The Page's name", max_length=200)),
      (
       b'link', models.URLField(help_text=b'Link to the page on Facebook', max_length=1000)),
      (
       b'is_published', models.BooleanField(default=False, help_text=b'Indicates whether the page is published and visible to non-admins')),
      (
       b'can_post', models.BooleanField(default=False, help_text=b'Indicates whether the current session user can post on this Page')),
      (
       b'location', annoying.fields.JSONField(help_text=b"The Page's street address, latitude, and longitude (when available)", null=True)),
      (
       b'cover', annoying.fields.JSONField(help_text=b'The JSON object including cover_id (the ID of the photo), source (the URL for the cover photo), and offset_y (the percentage offset from top [0-100])', null=True)),
      (
       b'likes_count', models.IntegerField(help_text=b'The number of users who like the Page', null=True)),
      (
       b'checkins_count', models.IntegerField(help_text=b'The total number of users who have checked in to the Page', null=True)),
      (
       b'talking_about_count', models.IntegerField(help_text=b'The number of people that are talking about this page (last seven days)', null=True)),
      (
       b'category', models.CharField(help_text=b"The Page's category", max_length=100)),
      (
       b'phone', models.CharField(help_text=b'The phone number (not always normalized for country code) for the Page', max_length=100)),
      (
       b'picture', models.CharField(help_text=b"Link to the Page's profile picture", max_length=100)),
      (
       b'website', models.CharField(help_text=b'Link to the external website for the page', max_length=1000)),
      (
       b'username', models.CharField(max_length=200)),
      (
       b'company_overview', models.TextField()),
      (
       b'about', models.TextField()),
      (
       b'products', models.TextField()),
      (
       b'description', models.TextField()),
      (
       b'posts_count', models.IntegerField(default=0))], options={b'verbose_name': b'Facebook page', 
        b'verbose_name_plural': b'Facebook pages'}, bases=(
      models.Model,))]