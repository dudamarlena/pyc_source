# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Volumes/Bucket/projects/tinymce/gu-django-tinymce/testtinymce/migrations/0001_initial.py
# Compiled at: 2016-04-21 01:49:54
from __future__ import unicode_literals
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
     migrations.CreateModel(name=b'TestInline', fields=[
      (
       b'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name=b'ID')),
      (
       b'content1', models.TextField()),
      (
       b'content2', models.TextField())]),
     migrations.CreateModel(name=b'TestPage', fields=[
      (
       b'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name=b'ID')),
      (
       b'content1', models.TextField()),
      (
       b'content2', models.TextField())]),
     migrations.AddField(model_name=b'testinline', name=b'page', field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=b'testtinymce.TestPage'))]