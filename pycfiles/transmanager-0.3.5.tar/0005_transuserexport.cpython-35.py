# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /var/www/transmanager/transmanager/migrations/0005_transuserexport.py
# Compiled at: 2016-09-19 04:59:30
# Size of source mod 2**32: 1247 bytes
from __future__ import unicode_literals
from django.db import migrations, models
import uuid
from django.conf import settings
import transmanager.models

class Migration(migrations.Migration):
    dependencies = [
     migrations.swappable_dependency(settings.AUTH_USER_MODEL),
     ('transmanager', '0004_transtask_content_type')]
    operations = [
     migrations.CreateModel(name='TransUserExport', fields=[
      (
       'id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
      (
       'file', models.FileField(max_length=255, blank=True, upload_to=transmanager.models.TransUserExport.upload_path, null=True)),
      (
       'creation_date', models.DateTimeField(auto_now_add=True, verbose_name='creation date')),
      (
       'uuid', models.UUIDField(default=uuid.uuid4, unique=True, verbose_name='Unique identifier')),
      (
       'user', models.ForeignKey(related_name='exports', verbose_name='usuario', to=settings.AUTH_USER_MODEL))], options={'verbose_name': 'User export', 
      'verbose_name_plural': 'User exports'})]