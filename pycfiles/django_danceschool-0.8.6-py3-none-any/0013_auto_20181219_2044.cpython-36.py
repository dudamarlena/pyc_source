# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /c/Users/Lee/Sync/projects/django-danceschool/currentmaster/django-danceschool/danceschool/financial/migrations/0013_auto_20181219_2044.py
# Compiled at: 2019-04-03 22:56:30
# Size of source mod 2**32: 1118 bytes
from __future__ import unicode_literals
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
     ('financial', '0012_auto_20181216_1615')]
    operations = [
     migrations.RemoveField(model_name='expenseitem',
       name='payToLocation'),
     migrations.RemoveField(model_name='expenseitem',
       name='payToName'),
     migrations.RemoveField(model_name='expenseitem',
       name='payToUser'),
     migrations.RemoveField(model_name='genericrepeatedexpense',
       name='payToLocation'),
     migrations.RemoveField(model_name='genericrepeatedexpense',
       name='payToName'),
     migrations.RemoveField(model_name='genericrepeatedexpense',
       name='payToUser'),
     migrations.RemoveField(model_name='revenueitem',
       name='receivedFromName')]