# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dyn_struct/migrations/0005_auto_20160913_1041.py
# Compiled at: 2016-09-13 03:41:52
# Size of source mod 2**32: 605 bytes
from __future__ import unicode_literals
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
     ('dyn_struct', '0004_auto_20160912_1752')]
    operations = [
     migrations.AlterModelOptions(name='dynamicstructurefield',
       options={'ordering':('structure__name', 'row', 'position'), 
      'verbose_name':'поле динамической структуры',  'verbose_name_plural':'поля динамических структур'})]