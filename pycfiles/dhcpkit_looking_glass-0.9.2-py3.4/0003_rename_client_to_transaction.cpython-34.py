# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/dhcpkit_looking_glass/migrations/0003_rename_client_to_transaction.py
# Compiled at: 2016-07-18 16:39:48
# Size of source mod 2**32: 516 bytes
from __future__ import unicode_literals
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
     ('dhcpkit_looking_glass', '0002_auto_20151110_0017')]
    operations = [
     migrations.RenameModel(old_name='Client', new_name='Transaction'),
     migrations.AlterModelTable(name='transaction', table=None)]