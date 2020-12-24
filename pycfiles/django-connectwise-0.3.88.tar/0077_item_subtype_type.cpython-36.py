# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/cameron/Dev/kanban-dev/django-connectwise/djconnectwise/migrations/0077_item_subtype_type.py
# Compiled at: 2019-05-14 12:25:52
# Size of source mod 2**32: 2653 bytes
from django.db import migrations, models
import django.db.models.deletion, django_extensions.db.fields

class Migration(migrations.Migration):
    dependencies = [
     ('djconnectwise', '0076_auto_20180925_1618')]
    operations = [
     migrations.CreateModel(name='Item',
       fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
      (
       'modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
      (
       'name', models.CharField(max_length=50)),
      (
       'board', models.ForeignKey(on_delete=(django.db.models.deletion.CASCADE), to='djconnectwise.ConnectWiseBoard'))],
       options={'verbose_name_plural':'Items', 
      'verbose_name':'Item'}),
     migrations.CreateModel(name='SubType',
       fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
      (
       'modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
      (
       'name', models.CharField(max_length=50)),
      (
       'board', models.ForeignKey(on_delete=(django.db.models.deletion.CASCADE), to='djconnectwise.ConnectWiseBoard'))],
       options={'verbose_name_plural':'Sub types', 
      'verbose_name':'Sub Type'}),
     migrations.CreateModel(name='Type',
       fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
      (
       'modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
      (
       'name', models.CharField(max_length=50)),
      (
       'board', models.ForeignKey(on_delete=(django.db.models.deletion.CASCADE), to='djconnectwise.ConnectWiseBoard'))],
       options={'verbose_name_plural':'Types', 
      'verbose_name':'Type'})]