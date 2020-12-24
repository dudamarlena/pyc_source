# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/silly/dev/django-category/category/migrations/0001_initial.py
# Compiled at: 2019-01-03 06:09:58
# Size of source mod 2**32: 2271 bytes
from __future__ import unicode_literals
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    initial = True
    dependencies = [
     ('sites', '0002_alter_domain_unique')]
    operations = [
     migrations.CreateModel(name='Category',
       fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'title', models.CharField(help_text=b'Short descriptive name for this category.', max_length=200)),
      (
       'subtitle', models.CharField(blank=True, default=b'', help_text=b'Some titles may be the same and cause confusion in admin UI. A subtitle makes a distinction.', max_length=200, null=True)),
      (
       'slug', models.SlugField(help_text=b'Short descriptive unique name for use in urls.', max_length=255, unique=True)),
      (
       'parent', models.ForeignKey(blank=True, null=True, on_delete=(django.db.models.deletion.CASCADE), to='category.Category')),
      (
       'sites', models.ManyToManyField(blank=True, help_text=b'Limits category scope to selected sites.', null=True, to='sites.Site'))],
       options={'ordering':('title', ), 
      'verbose_name':'category', 
      'verbose_name_plural':'categories'}),
     migrations.CreateModel(name='Tag',
       fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'title', models.CharField(help_text=b'Short descriptive name for this tag.', max_length=200)),
      (
       'slug', models.SlugField(help_text=b'Short descriptive unique name for use in urls.', max_length=255, unique=True)),
      (
       'categories', models.ManyToManyField(blank=True, help_text=b'Categories to which this tag belongs.', null=True, to='category.Category'))],
       options={'ordering':('title', ), 
      'verbose_name':'tag', 
      'verbose_name_plural':'tags'})]