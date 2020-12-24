# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/link/migrations/0001_initial.py
# Compiled at: 2017-07-06 07:47:29
from __future__ import unicode_literals
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    initial = True
    dependencies = [
     ('contenttypes', '0002_remove_content_type_name')]
    operations = [
     migrations.CreateModel(name=b'Link', fields=[
      (
       b'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name=b'ID')),
      (
       b'title', models.CharField(help_text=b'A short descriptive title.', max_length=256)),
      (
       b'slug', models.SlugField(max_length=256)),
      (
       b'view_name', models.CharField(blank=True, help_text=b'View name to which this link will redirect.', max_length=256, null=True)),
      (
       b'target_object_id', models.PositiveIntegerField(blank=True, null=True)),
      (
       b'url', models.CharField(blank=True, help_text=b'URL to which this link will redirect.', max_length=256, null=True)),
      (
       b'target_content_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name=b'link_target_content_type', to=b'contenttypes.ContentType'))], options={b'ordering': [
                    b'title']})]