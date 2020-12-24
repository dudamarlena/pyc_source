# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/luisza/Escritorio/desarrollo/djreservation/djreservation/migrations/0005_reservationtoken.py
# Compiled at: 2019-02-19 21:49:51
# Size of source mod 2**32: 790 bytes
from __future__ import unicode_literals
from django.db import migrations, models
import django.db.models.deletion, uuid

class Migration(migrations.Migration):
    dependencies = [
     ('djreservation', '0004_auto_20161005_0022')]
    operations = [
     migrations.CreateModel(name='ReservationToken', fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'token', models.UUIDField(default=uuid.uuid4, editable=False)),
      (
       'reservation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='djreservation.Reservation'))])]