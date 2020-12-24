# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nicolas/dev/feedpubsub/reader/migrations/0010_cachedimage.py
# Compiled at: 2018-09-28 06:25:38
# Size of source mod 2**32: 1105 bytes
from django.db import migrations, models
import uuid

class Migration(migrations.Migration):
    dependencies = [
     ('reader', '0009_auto_20180918_1143')]
    operations = [
     migrations.CreateModel(name='CachedImage',
       fields=[
      (
       'id', models.UUIDField(default=(uuid.uuid4), editable=False, primary_key=True, serialize=False)),
      (
       'uri', models.URLField(db_index=True, max_length=400, unique=True)),
      (
       'format', models.CharField(blank=True, default='', editable=False, max_length=8)),
      (
       'width', models.PositiveSmallIntegerField(default=0, editable=False)),
      (
       'height', models.PositiveSmallIntegerField(default=0, editable=False)),
      (
       'size_in_bytes', models.PositiveIntegerField(default=0, editable=False)),
      (
       'failure_reason', models.CharField(blank=True, default='', editable=False, max_length=100)),
      (
       'created_at', models.DateTimeField(auto_now_add=True))])]