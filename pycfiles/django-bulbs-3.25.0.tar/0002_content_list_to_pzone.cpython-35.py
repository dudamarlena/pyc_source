# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /webapp/bulbs/promotion/migrations/0002_content_list_to_pzone.py
# Compiled at: 2016-09-22 15:00:17
# Size of source mod 2**32: 4862 bytes
from __future__ import unicode_literals
from django.db import models, migrations
import json_field.fields

class Migration(migrations.Migration):
    dependencies = [
     ('contenttypes', '0001_initial'),
     ('content', '0001_initial'),
     ('promotion', '0001_initial')]
    operations = [
     migrations.DeleteModel(name='LockOperation'),
     migrations.DeleteModel(name='UnlockOperation'),
     migrations.DeleteModel(name='InsertOperation'),
     migrations.DeleteModel(name='ReplaceOperation'),
     migrations.DeleteModel(name='ContentListOperation'),
     migrations.DeleteModel(name='ContentListHistory'),
     migrations.RenameModel(old_name='ContentList', new_name='PZone'),
     migrations.RenameField(model_name='pzone', old_name='length', new_name='zone_length'),
     migrations.CreateModel(name='PZoneOperation', fields=[
      (
       'id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
      (
       'when', models.DateTimeField()),
      (
       'applied', models.BooleanField(default=False))], options={'ordering': ['-when', 'id']}, bases=(
      models.Model,)),
     migrations.AddField(model_name='pzoneoperation', name='content', field=models.ForeignKey(related_name='+', to='content.Content'), preserve_default=True),
     migrations.AddField(model_name='pzoneoperation', name='polymorphic_ctype', field=models.ForeignKey(related_name='polymorphic_promotion.pzoneoperation_set', editable=False, to='contenttypes.ContentType', null=True), preserve_default=True),
     migrations.AddField(model_name='pzoneoperation', name='pzone', field=models.ForeignKey(related_name='operations', to='promotion.PZone'), preserve_default=True),
     migrations.CreateModel(name='DeleteOperation', fields=[
      (
       'pzoneoperation_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='promotion.PZoneOperation'))], options={'abstract': False}, bases=('promotion.pzoneoperation', )),
     migrations.CreateModel(name='InsertOperation', fields=[
      (
       'pzoneoperation_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='promotion.PZoneOperation'))], options={'abstract': False}, bases=('promotion.pzoneoperation', )),
     migrations.AddField(model_name='insertoperation', name='index', field=models.IntegerField(default=0), preserve_default=True),
     migrations.CreateModel(name='ReplaceOperation', fields=[
      (
       'pzoneoperation_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='promotion.PZoneOperation'))], options={'abstract': False}, bases=('promotion.pzoneoperation', )),
     migrations.AddField(model_name='replaceoperation', name='index', field=models.IntegerField(default=0), preserve_default=True),
     migrations.CreateModel(name='PZoneHistory', fields=[
      (
       'id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
      (
       'data', json_field.fields.JSONField(default=[], help_text='Enter a valid JSON object')),
      (
       'date', models.DateTimeField(auto_now_add=True))], options={}, bases=(
      models.Model,)),
     migrations.AddField(model_name='pzonehistory', name='pzone', field=models.ForeignKey(related_name='history', to='promotion.PZone'), preserve_default=True)]