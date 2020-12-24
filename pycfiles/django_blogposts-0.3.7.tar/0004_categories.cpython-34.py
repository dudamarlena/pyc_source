# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /vagrant/django_blogposts/django_blogposts/migrations/0004_categories.py
# Compiled at: 2018-08-06 04:08:22
# Size of source mod 2**32: 1279 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('django_blogposts', '0003_auto_20160210_0934')]
    operations = [
     migrations.CreateModel(name='Categories', fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'name', models.CharField(max_length=400, verbose_name='Name')),
      (
       'slug', models.CharField(max_length=100, verbose_name='Slug')),
      (
       'content', models.TextField(blank=True, null=True, verbose_name='Short description of category (if needed)')),
      (
       'is_moderated', models.BooleanField(default=True, verbose_name='Is moderated')),
      (
       'da', models.DateTimeField(auto_now_add=True, verbose_name='Date of create')),
      (
       'de', models.DateTimeField(auto_now=True, verbose_name='Date of last edit'))], options={'ordering': [
                   '-da'], 
      'verbose_name': 'Category', 
      'verbose_name_plural': 'Categories'})]