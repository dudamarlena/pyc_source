# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/explore/migrations/0001_initial.py
# Compiled at: 2020-05-05 16:46:09
# Size of source mod 2**32: 1827 bytes
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
     migrations.CreateModel(name='Corpus',
       fields=[
      (
       'id',
       models.AutoField(auto_created=True,
         primary_key=True,
         serialize=False,
         verbose_name='ID')),
      (
       'slug', models.SlugField(max_length=255)),
      (
       'language', models.CharField(max_length=255)),
      (
       'path', models.TextField()),
      (
       'desc', models.TextField(default='')),
      (
       'len', models.BigIntegerField()),
      (
       'diabled', models.BooleanField(default=False)),
      (
       'date', models.DateField()),
      (
       'load', models.BooleanField(default=True)),
      (
       'url', models.URLField(max_length=255))]),
     migrations.CreateModel(name='DropColumn',
       fields=[
      (
       'id',
       models.AutoField(auto_created=True,
         primary_key=True,
         serialize=False,
         verbose_name='ID')),
      (
       'column_name', models.CharField(max_length=255)),
      (
       'corpus',
       models.ForeignKey(on_delete=(django.db.models.deletion.CASCADE),
         to='explore.Corpus'))])]