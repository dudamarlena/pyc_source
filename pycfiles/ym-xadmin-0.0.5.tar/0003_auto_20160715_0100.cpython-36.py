# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: G:\python\hhwork\extra_apps\xadmin\migrations\0003_auto_20160715_0100.py
# Compiled at: 2018-12-16 22:27:14
# Size of source mod 2**32: 464 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('xadmin', '0002_log')]
    operations = [
     migrations.AlterField(model_name='log',
       name='action_flag',
       field=models.CharField(max_length=32, verbose_name='action flag'))]