# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./../tablets/migrations/0002_add_mptt.py
# Compiled at: 2019-01-24 09:14:36
# Size of source mod 2**32: 1695 bytes
from __future__ import unicode_literals
from django.db import models, migrations
import mptt.fields

class Migration(migrations.Migration):
    dependencies = [
     ('tablets', '0001_initial')]
    operations = [
     migrations.AlterModelOptions(name='template',
       options={'ordering':('name', ), 
      'verbose_name':'Template',  'verbose_name_plural':'Templates'}),
     migrations.AddField(model_name='template',
       name='level',
       field=models.PositiveIntegerField(default=1, editable=False, db_index=True),
       preserve_default=False),
     migrations.AddField(model_name='template',
       name='lft',
       field=models.PositiveIntegerField(default=1, editable=False, db_index=True),
       preserve_default=False),
     migrations.AddField(model_name='template',
       name='rght',
       field=models.PositiveIntegerField(default=1, editable=False, db_index=True),
       preserve_default=False),
     migrations.AddField(model_name='template',
       name='tree_id',
       field=models.PositiveIntegerField(default=1, editable=False, db_index=True),
       preserve_default=False),
     migrations.AlterField(model_name='template',
       name='parent',
       field=mptt.fields.TreeForeignKey(related_name='children', blank=True, to='tablets.Template', help_text='Select another template this template should extend.', null=True, on_delete=(models.CASCADE)),
       preserve_default=True)]