# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\dipap\Desktop\Projects\Orfium\project\earnings-dashboard\upload_tools\migrations\0001_initial.py
# Compiled at: 2017-12-07 10:12:17
from __future__ import unicode_literals
from django.db import migrations, models
import django.db.models.deletion, s3direct.fields, uuid

class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
     migrations.CreateModel(name=b'UploadJob', fields=[
      (
       b'id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, unique=True)),
      (
       b'created', models.DateTimeField(auto_now_add=True)),
      (
       b'updated', models.DateTimeField(auto_now_add=True)),
      (
       b'started', models.DateTimeField(blank=True, default=None, null=True)),
      (
       b'finished', models.DateTimeField(blank=True, default=None, null=True)),
      (
       b'info', models.TextField(blank=True, default=None, null=True)),
      (
       b'upload_type', models.CharField(max_length=32)),
      (
       b'status', models.CharField(choices=[('SUBMITTED', 'Submitted'), ('STARTED', 'Started'), ('FINISHED', 'Finished'), ('FAILED', 'Failed')], default=b'SUBMITTED', max_length=32))]),
     migrations.CreateModel(name=b'AssetUploadJob', fields=[
      (
       b'uploadjob_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=b'upload_tools.UploadJob')),
      (
       b'asset_file', s3direct.fields.S3DirectField(help_text=b'Upload the CSV file with the assets.\nFormat:\nAsset Title,Asset Type,Orfium ID,UPC,EAN,ISAN,ISRC,ISWC,GRID\nRequires the header line (use the line above).\nUse " as the quote character and , to separate columns.'))], bases=('upload_tools.uploadjob', ))]