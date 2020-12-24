# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dyn_struct/migrations/0002_auto_20160831_2238.py
# Compiled at: 2016-08-31 15:38:55
# Size of source mod 2**32: 615 bytes
from __future__ import unicode_literals
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('dyn_struct', '0001_initial')]
    operations = [
     migrations.AlterField(model_name='dynamicstructurefield',
       name='structure',
       field=models.ForeignKey(on_delete=(django.db.models.deletion.CASCADE), related_name='fields', to='dyn_struct.DynamicStructure', verbose_name='Структура'))]