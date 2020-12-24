# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/luisza/Escritorio/desarrollo/djreservation/djreservation/migrations/0004_auto_20161005_0022.py
# Compiled at: 2019-02-19 21:49:51
# Size of source mod 2**32: 455 bytes
from __future__ import unicode_literals
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
     ('djreservation', '0003_auto_20161004_1525')]
    operations = [
     migrations.RenameField(model_name='reservation', old_name='return_date', new_name='reserved_end_date')]