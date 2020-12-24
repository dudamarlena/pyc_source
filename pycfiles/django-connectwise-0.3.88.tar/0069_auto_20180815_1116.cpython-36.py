# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/cameron/Dev/kanban-dev/django-connectwise/djconnectwise/migrations/0069_auto_20180815_1116.py
# Compiled at: 2019-05-14 12:25:52
# Size of source mod 2**32: 832 bytes
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('djconnectwise', '0068_merge_20180814_1104')]
    operations = [
     migrations.AlterField(model_name='timeentry',
       name='billable_option',
       field=models.CharField(choices=[('Billable', 'Billable'), ('DoNotBill', 'Do Not Bill'), ('NoCharge', 'No Charge'), ('NoDefault', 'No Default')], max_length=250)),
     migrations.AlterField(model_name='timeentry',
       name='charge_to_type',
       field=models.CharField(choices=[('ServiceTicket', 'Service Ticket'), ('ProjectTicket', 'Project Ticket'), ('ChargeCode', 'Charge Code'), ('Activity', 'Activity')], max_length=250))]