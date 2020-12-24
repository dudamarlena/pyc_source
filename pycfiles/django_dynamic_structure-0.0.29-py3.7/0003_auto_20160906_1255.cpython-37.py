# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dyn_struct/migrations/0003_auto_20160906_1255.py
# Compiled at: 2016-09-06 05:55:26
# Size of source mod 2**32: 1517 bytes
from __future__ import unicode_literals
from django.db import migrations, models
import dyn_struct.db.fields

class Migration(migrations.Migration):
    dependencies = [
     ('dyn_struct', '0002_auto_20160831_2238')]
    operations = [
     migrations.AlterField(model_name='dynamicstructurefield',
       name='form_kwargs',
       field=dyn_struct.db.fields.ParamsField(default='{}', verbose_name='Параметры поля')),
     migrations.AlterField(model_name='dynamicstructurefield',
       name='header',
       field=models.CharField(blank=True, help_text='при заполнении этого поля, вместо поля формы будет выводить заголовок', max_length=100, verbose_name='заголовок')),
     migrations.AlterField(model_name='dynamicstructurefield',
       name='name',
       field=models.CharField(blank=True, max_length=100, verbose_name='Название')),
     migrations.AlterField(model_name='dynamicstructurefield',
       name='widget_kwargs',
       field=dyn_struct.db.fields.ParamsField(default='{}', verbose_name='Параметры виджета')),
     migrations.AlterUniqueTogether(name='dynamicstructurefield',
       unique_together=(set([('name', 'header')])))]