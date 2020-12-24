# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dyn_struct/migrations/0006_auto_20200117_2316.py
# Compiled at: 2020-01-18 04:29:05
# Size of source mod 2**32: 446 bytes
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('dyn_struct', '0005_auto_20160913_1041')]
    operations = [
     migrations.AlterField(model_name='dynamicstructurefield',
       name='name',
       field=models.CharField(blank=True, max_length=512, verbose_name='Название'))]