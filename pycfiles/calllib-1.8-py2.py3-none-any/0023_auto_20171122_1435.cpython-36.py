# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/Ari/src/callisto-core/callisto_core/delivery/migrations/0023_auto_20171122_1435.py
# Compiled at: 2019-08-07 16:42:06
# Size of source mod 2**32: 836 bytes
from __future__ import unicode_literals
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
     ('delivery', '0022_auto_20171122_1434')]
    operations = [
     migrations.RenameField(model_name='sentfullreport',
       old_name='new_sent',
       new_name='sent'),
     migrations.RenameField(model_name='sentfullreport',
       old_name='new_to_address',
       new_name='to_address'),
     migrations.RenameField(model_name='sentmatchreport',
       old_name='new_sent',
       new_name='sent'),
     migrations.RenameField(model_name='sentmatchreport',
       old_name='new_to_address',
       new_name='to_address')]