# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-intel/egg/forman/migrations/0001_initial.py
# Compiled at: 2017-05-08 12:16:33
from __future__ import unicode_literals
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    initial = True
    dependencies = [
     ('campaigns', '0005_auto_20170402_1412')]
    operations = [
     migrations.CreateModel(name=b'Input', fields=[
      (
       b'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name=b'ID')),
      (
       b'title', models.CharField(max_length=200)),
      (
       b'display_type', models.CharField(choices=[('text', 'text'), ('file', 'file'), ('select', 'select'), ('multi-select', 'multi-select'), ('checkbox', 'checkbox')], max_length=100)),
      (
       b'predefined_values', models.TextField(blank=True, null=True))]),
     migrations.CreateModel(name=b'Survey', fields=[
      (
       b'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name=b'ID')),
      (
       b'header_message', models.CharField(max_length=200)),
      (
       b'header_image', models.FileField(upload_to=b'')),
      (
       b'ad', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=b'campaigns.Ad'))]),
     migrations.AddField(model_name=b'input', name=b'survey', field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=b'forman.Survey'))]