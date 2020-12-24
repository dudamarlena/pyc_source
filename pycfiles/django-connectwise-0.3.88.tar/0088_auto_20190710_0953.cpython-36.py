# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/cameron/Dev/kanban-dev/django-connectwise/djconnectwise/migrations/0088_auto_20190710_0953.py
# Compiled at: 2019-07-11 13:48:16
# Size of source mod 2**32: 496 bytes
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('djconnectwise', '0087_auto_20190705_1015')]
    operations = [
     migrations.AlterField(model_name='timeentry',
       name='billable_option',
       field=models.CharField(choices=[('Billable', 'Billable'), ('DoNotBill', 'Do Not Bill'), ('NoCharge', 'No Charge')], max_length=250))]