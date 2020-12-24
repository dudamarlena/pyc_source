# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/arroyo/ovp/gpa-ovp/django-react-cms/react_cms/migrations/0002_contentresource.py
# Compiled at: 2017-01-09 13:04:21
# Size of source mod 2**32: 809 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    initial = True
    dependencies = [
     ('react_cms', '0001_initial')]
    operations = [
     migrations.CreateModel(name='ContentResource', fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'name', models.CharField(max_length=100, verbose_name='Resource Name')),
      (
       'path', models.CharField(max_length=1000, verbose_name='Resource Path')),
      (
       'json', models.TextField(blank=True, null=True, verbose_name='Label'))])]