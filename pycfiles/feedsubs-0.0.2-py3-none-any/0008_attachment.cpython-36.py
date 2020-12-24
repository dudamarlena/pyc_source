# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nicolas/dev/feedpubsub/reader/migrations/0008_attachment.py
# Compiled at: 2018-09-15 11:39:04
# Size of source mod 2**32: 958 bytes
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('reader', '0007_auto_20180913_2004')]
    operations = [
     migrations.CreateModel(name='Attachment',
       fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'uri', models.URLField(max_length=400)),
      (
       'title', models.TextField(blank=True)),
      (
       'mime_type', models.CharField(blank=True, max_length=100)),
      (
       'size_in_bytes', models.PositiveIntegerField(blank=True, null=True)),
      (
       'duration', models.DurationField(blank=True, null=True)),
      (
       'article', models.ForeignKey(on_delete=(django.db.models.deletion.CASCADE), to='reader.Article'))])]