# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/flanker/Developer/Github/Moneta/moneta/repository/migrations/0006_auto_20171104_1444.py
# Compiled at: 2017-11-04 09:44:29
# Size of source mod 2**32: 464 bytes
from __future__ import unicode_literals
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
     ('repository', '0005_auto_20171104_1300')]
    operations = [
     migrations.AlterModelOptions(name='repository',
       options={'verbose_name':'repository', 
      'verbose_name_plural':'repositories'})]