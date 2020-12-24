# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/luisza/Escritorio/desarrollo/djreservation/djreservation/migrations/0003_auto_20161004_1525.py
# Compiled at: 2019-02-19 21:49:51
# Size of source mod 2**32: 576 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('djreservation', '0002_auto_20160903_0030')]
    operations = [
     migrations.AlterField(model_name='reservation', name='status', field=models.SmallIntegerField(choices=[(0, 'Building'), (1, 'Requested'), (2, 'Acepted'), (3, 'Denied'), (4, 'Borrowed'), (5, 'Returned')], default=0))]