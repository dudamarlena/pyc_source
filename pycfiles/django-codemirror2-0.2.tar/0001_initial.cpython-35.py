# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/alex/source/git/django-codemirror2/examples/testapp/migrations/0001_initial.py
# Compiled at: 2016-02-02 21:54:34
# Size of source mod 2**32: 927 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
     migrations.CreateModel(name='TestCss', fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'title', models.CharField(max_length=255)),
      (
       'css', models.TextField())]),
     migrations.CreateModel(name='TestHTML', fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'title', models.CharField(max_length=255)),
      (
       'html', models.TextField())])]