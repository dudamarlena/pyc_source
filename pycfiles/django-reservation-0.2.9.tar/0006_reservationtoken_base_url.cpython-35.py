# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/luisza/Escritorio/desarrollo/djreservation/djreservation/migrations/0006_reservationtoken_base_url.py
# Compiled at: 2019-02-19 21:49:51
# Size of source mod 2**32: 482 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('djreservation', '0005_reservationtoken')]
    operations = [
     migrations.AddField(model_name='reservationtoken', name='base_url', field=models.URLField(default='http://localhost:8000'))]