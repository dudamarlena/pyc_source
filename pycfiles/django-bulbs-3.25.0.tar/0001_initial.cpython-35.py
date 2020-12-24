# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /webapp/bulbs/videos/migrations/0001_initial.py
# Compiled at: 2016-09-22 15:00:17
# Size of source mod 2**32: 1147 bytes
from __future__ import unicode_literals
from django.db import migrations, models
import djbetty.fields

class Migration(migrations.Migration):
    dependencies = []
    operations = [
     migrations.CreateModel(name='VideohubVideo', fields=[
      (
       'id', models.IntegerField(serialize=False, primary_key=True)),
      (
       'title', models.CharField(max_length=512)),
      (
       'description', models.TextField(blank=True, default='')),
      (
       'keywords', models.TextField(blank=True, default='')),
      (
       'image', djbetty.fields.ImageField(blank=True, null=True, alt_field='_image_alt', default=None, caption_field='_image_caption')),
      (
       '_image_alt', models.CharField(blank=True, null=True, max_length=255, editable=False)),
      (
       '_image_caption', models.CharField(blank=True, null=True, max_length=255, editable=False)),
      (
       'channel_id', models.IntegerField(blank=True, null=True, default=None))], options={'abstract': False})]