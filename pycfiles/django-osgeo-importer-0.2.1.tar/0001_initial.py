# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /mnt/importer/osgeo_importer/migrations/0001_initial.py
# Compiled at: 2016-07-18 17:07:14
from __future__ import unicode_literals
from django.db import models, migrations
from django.conf import settings
import jsonfield.fields, osgeo_importer.models

class Migration(migrations.Migration):
    dependencies = [
     ('contenttypes', '0002_remove_content_type_name'),
     migrations.swappable_dependency(settings.AUTH_USER_MODEL)]
    operations = [
     migrations.CreateModel(name=b'UploadedData', fields=[
      (
       b'id', models.AutoField(verbose_name=b'ID', serialize=False, auto_created=True, primary_key=True)),
      (
       b'state', models.CharField(max_length=16)),
      (
       b'date', models.DateTimeField(auto_now_add=True, verbose_name=b'date')),
      (
       b'upload_dir', models.CharField(max_length=100, null=True)),
      (
       b'name', models.CharField(max_length=64, null=True)),
      (
       b'complete', models.BooleanField(default=False)),
      (
       b'size', models.IntegerField(null=True, blank=True)),
      (
       b'metadata', models.TextField(null=True)),
      (
       b'file_type', models.CharField(max_length=50, null=True, blank=True)),
      (
       b'user', models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True))], options={b'ordering': [
                    b'-date'], 
        b'verbose_name_plural': b'Upload data'}),
     migrations.CreateModel(name=b'UploadException', fields=[
      (
       b'id', models.AutoField(verbose_name=b'ID', serialize=False, auto_created=True, primary_key=True)),
      (
       b'created_at', models.DateTimeField(auto_now_add=True, verbose_name=b'Timestamp when the exception was logged.')),
      (
       b'task_id', models.CharField(max_length=36, null=True, blank=True)),
      (
       b'traceback', models.TextField(null=True, blank=True)),
      (
       b'verbose_traceback', models.TextField(help_text=b'A humanized exception message.', null=True, blank=True))], options={b'verbose_name': b'Upload Exception'}),
     migrations.CreateModel(name=b'UploadFile', fields=[
      (
       b'id', models.AutoField(verbose_name=b'ID', serialize=False, auto_created=True, primary_key=True)),
      (
       b'file', models.FileField(upload_to=b'uploads', validators=[osgeo_importer.models.validate_file_extension, osgeo_importer.models.validate_inspector_can_read])),
      (
       b'slug', models.SlugField(max_length=250, blank=True)),
      (
       b'upload', models.ForeignKey(blank=True, to=b'osgeo_importer.UploadedData', null=True))]),
     migrations.CreateModel(name=b'UploadLayer', fields=[
      (
       b'id', models.AutoField(verbose_name=b'ID', serialize=False, auto_created=True, primary_key=True)),
      (
       b'index', models.IntegerField(default=0)),
      (
       b'name', models.CharField(max_length=64, null=True)),
      (
       b'fields', jsonfield.fields.JSONField(null=True)),
      (
       b'object_id', models.PositiveIntegerField(null=True, blank=True)),
      (
       b'configuration_options', jsonfield.fields.JSONField(null=True)),
      (
       b'task_id', models.CharField(max_length=36, null=True, blank=True)),
      (
       b'feature_count', models.IntegerField(null=True, blank=True)),
      (
       b'content_type', models.ForeignKey(blank=True, to=b'contenttypes.ContentType', null=True)),
      (
       b'upload', models.ForeignKey(blank=True, to=b'osgeo_importer.UploadedData', null=True))], options={b'ordering': ('index', )}),
     migrations.AddField(model_name=b'uploadexception', name=b'upload_layer', field=models.ForeignKey(blank=True, to=b'osgeo_importer.UploadLayer', null=True))]