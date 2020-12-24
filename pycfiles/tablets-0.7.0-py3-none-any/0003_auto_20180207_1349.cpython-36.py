# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./../tablets/migrations/0003_auto_20180207_1349.py
# Compiled at: 2018-02-08 11:27:45
# Size of source mod 2**32: 445 bytes
from __future__ import unicode_literals
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
     ('tablets', '0002_add_mptt')]
    operations = [
     migrations.AlterModelOptions(name='template',
       options={'verbose_name':'Template', 
      'verbose_name_plural':'Templates'})]