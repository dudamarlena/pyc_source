# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mathias/tbp/django_rxncon_site/src/rule_based/migrations/0001_initial.py
# Compiled at: 2018-06-27 10:59:30
# Size of source mod 2**32: 1010 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
     migrations.CreateModel(name='Rule_based_from_rxnconsys', fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'project_name', models.CharField(max_length=120)),
      (
       'slug', models.SlugField(blank=True)),
      (
       'comment', models.TextField(blank=True, null=True)),
      (
       'timestamp', models.DateTimeField(auto_now_add=True)),
      (
       'updated', models.DateTimeField(auto_now=True)),
      (
       'model_path', models.FileField(null=True, upload_to=''))], options={'ordering': ['-updated', '-timestamp']})]