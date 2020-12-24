# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/areski/projects/django/django-audiofield/audiofield/migrations/0001_initial.py
# Compiled at: 2015-12-15 09:52:28
from __future__ import unicode_literals
import audiofield.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    initial = True
    dependencies = [
     migrations.swappable_dependency(settings.AUTH_USER_MODEL)]
    operations = [
     migrations.CreateModel(name=b'AudioFile', fields=[
      (
       b'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name=b'ID')),
      (
       b'name', models.CharField(help_text=b'audio file label', max_length=150, verbose_name=b'audio name')),
      (
       b'audio_file', audiofield.fields.AudioField(blank=True, upload_to=b'upload/audiofiles', verbose_name=b'audio file')),
      (
       b'created_date', models.DateTimeField(auto_now_add=True)),
      (
       b'updated_date', models.DateTimeField(auto_now=True)),
      (
       b'user', models.ForeignKey(help_text=b'select user', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name=b'user'))], options={b'db_table': b'audio_file', 
        b'verbose_name': b'audio file', 
        b'verbose_name_plural': b'audio files', 
        b'permissions': (('view_audiofile', 'can see Audio Files'), )})]