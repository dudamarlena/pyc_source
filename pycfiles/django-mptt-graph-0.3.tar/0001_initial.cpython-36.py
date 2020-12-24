# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ggg/dev/django/django2/django2/mptt_graph/migrations/0001_initial.py
# Compiled at: 2018-02-15 04:18:06
# Size of source mod 2**32: 2091 bytes
from __future__ import unicode_literals
from django.db import migrations, models
import django.db.models.deletion, mptt.fields

class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
     migrations.CreateModel(name='GraphModel',
       fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'title', models.CharField(max_length=200, verbose_name='Title')),
      (
       'model_path', models.CharField(help_text='Path to the model: ex: myapp.models.MyModel', max_length=200, verbose_name='Model path')),
      (
       'model_pk', models.PositiveSmallIntegerField(verbose_name='Root node primary key'))],
       options={'verbose_name_plural':'Mptt graphs', 
      'ordering':('title', ), 
      'verbose_name':'Mptt graph'}),
     migrations.CreateModel(name='TreeNode',
       fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'title', models.CharField(max_length=200, verbose_name='Title')),
      (
       'lft', models.PositiveIntegerField(db_index=True, editable=False)),
      (
       'rght', models.PositiveIntegerField(db_index=True, editable=False)),
      (
       'tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
      (
       'level', models.PositiveIntegerField(db_index=True, editable=False)),
      (
       'parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=(django.db.models.deletion.CASCADE), related_name='children', to='mptt_graph.TreeNode', verbose_name='Parent node'))],
       options={'verbose_name_plural':'Tree nodes', 
      'ordering':('title', ), 
      'verbose_name':'Tree node'})]