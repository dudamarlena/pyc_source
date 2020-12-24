# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/jojo/workspace/locations/src/unicef_locations/migrations/0004_pcode_remap_related.py
# Compiled at: 2019-04-19 21:07:17
# Size of source mod 2**32: 1788 bytes
from __future__ import unicode_literals
import django.db.models.deletion, django.utils.timezone, model_utils.fields
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('locations', '0003_make_not_nullable'),
     ('contenttypes', '0001_initial')]
    operations = [
     migrations.AddField(model_name='cartodbtable',
       name='remap_table_name',
       field=models.CharField(blank=True, max_length=254, null=True, verbose_name='Remap Table Name')),
     migrations.AddField(model_name='location',
       name='is_active',
       field=models.BooleanField(default=True, verbose_name='Active')),
     migrations.CreateModel(name='LocationRemapHistory',
       fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'comments', models.TextField(blank=True, null=True, verbose_name='Comments')),
      (
       'created',
       model_utils.fields.AutoCreatedField(default=(django.utils.timezone.now), editable=False, verbose_name='created')),
      (
       'new_location',
       models.ForeignKey(on_delete=(django.db.models.deletion.CASCADE), related_name='+', to='locations.Location',
         verbose_name='New Location')),
      (
       'old_location',
       models.ForeignKey(on_delete=(django.db.models.deletion.CASCADE), related_name='+', to='locations.Location',
         verbose_name='Old Location'))])]