# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dyn_struct/migrations/0004_auto_20160912_1752.py
# Compiled at: 2016-09-12 10:52:56
# Size of source mod 2**32: 1982 bytes
from __future__ import unicode_literals
from django.db import migrations, models
import django.utils.timezone

class Migration(migrations.Migration):
    dependencies = [
     ('dyn_struct', '0003_auto_20160906_1255')]
    operations = [
     migrations.AlterModelOptions(name='dynamicstructurefield',
       options={'ordering':('row', 'position'), 
      'verbose_name':'поле динамической структуры',  'verbose_name_plural':'поля динамических структур'}),
     migrations.AddField(model_name='dynamicstructure',
       name='created',
       field=models.DateTimeField(auto_now_add=True, default=(django.utils.timezone.now)),
       preserve_default=False),
     migrations.AddField(model_name='dynamicstructure',
       name='is_deprecated',
       field=models.BooleanField(default=False, editable=False)),
     migrations.AddField(model_name='dynamicstructure',
       name='version',
       field=models.PositiveIntegerField(default=1, editable=False)),
     migrations.AddField(model_name='dynamicstructurefield',
       name='created',
       field=models.DateTimeField(auto_now_add=True, default=(django.utils.timezone.now)),
       preserve_default=False),
     migrations.AlterField(model_name='dynamicstructure',
       name='name',
       field=models.CharField(max_length=255, verbose_name='Название')),
     migrations.AlterUniqueTogether(name='dynamicstructure',
       unique_together=(set([('name', 'version')]))),
     migrations.AlterUniqueTogether(name='dynamicstructurefield',
       unique_together=(set([('structure', 'name', 'header')])))]