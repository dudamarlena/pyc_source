# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /vagrant/django_blogposts/django_blogposts/migrations/0001_initial.py
# Compiled at: 2018-08-06 04:08:22
# Size of source mod 2**32: 1588 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
     migrations.CreateModel(name='BlogPost', fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'meta_title', models.CharField(max_length=400, verbose_name='Meta-tag title')),
      (
       'meta_kw', models.CharField(max_length=400, verbose_name='Meta-tag keywords')),
      (
       'meta_desc', models.TextField(verbose_name='Meta-tag Description')),
      (
       'header', models.CharField(max_length=400, verbose_name='Header (tag H1)')),
      (
       'short_content', models.TextField(verbose_name='Short content for preview')),
      (
       'content', models.TextField(verbose_name='Content')),
      (
       'image', models.ImageField(upload_to=b'blog/%Y/%m/%d', verbose_name='Image')),
      (
       'is_moderated', models.BooleanField(default=False, verbose_name='Is moderated')),
      (
       'da', models.DateTimeField(auto_now_add=True, verbose_name='Date of create')),
      (
       'de', models.DateTimeField(auto_now=True, verbose_name='Date of last edit'))], options={'ordering': [
                   '-da'], 
      'verbose_name': 'Blog post', 
      'verbose_name_plural': 'Blog posts'})]