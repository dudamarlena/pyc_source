# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /vagrant/django_blogposts/django_blogposts/migrations/0002_auto_20160205_0923.py
# Compiled at: 2018-08-06 04:08:22
# Size of source mod 2**32: 681 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('django_blogposts', '0001_initial')]
    operations = [
     migrations.AddField(model_name='blogpost', name='slug', field=models.SlugField(blank=True, max_length=100, null=True, verbose_name='Slug')),
     migrations.AlterField(model_name='blogpost', name='is_moderated', field=models.BooleanField(default=True, verbose_name='Is moderated'))]