# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /vagrant/django_blogposts/django_blogposts/migrations/0006_auto_20160301_0905.py
# Compiled at: 2018-08-06 04:08:22
# Size of source mod 2**32: 1166 bytes
from __future__ import unicode_literals
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('django_blogposts', '0005_blogpost_category')]
    operations = [
     migrations.CreateModel(name='Tags', fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'name', models.CharField(max_length=400, verbose_name='Name')),
      (
       'slug', models.CharField(max_length=100, verbose_name='Slug')),
      (
       'is_moderated', models.BooleanField(default=True, verbose_name='Is moderated')),
      (
       'da', models.DateTimeField(auto_now_add=True, verbose_name='Date of create')),
      (
       'de', models.DateTimeField(auto_now=True, verbose_name='Date of last edit'))], options={'ordering': [
                   '-da'], 
      'verbose_name': 'Tag', 
      'verbose_name_plural': 'Tags'})]