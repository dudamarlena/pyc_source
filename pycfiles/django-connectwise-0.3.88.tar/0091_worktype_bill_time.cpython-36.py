# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/cameron/Dev/kanban-dev/django-connectwise/djconnectwise/migrations/0091_worktype_bill_time.py
# Compiled at: 2019-07-16 17:55:55
# Size of source mod 2**32: 509 bytes
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('djconnectwise', '0090_auto_20190711_1114')]
    operations = [
     migrations.AddField(model_name='worktype',
       name='bill_time',
       field=models.CharField(blank=True, choices=[('Billable', 'Billable'), ('DoNotBill', 'Do Not Bill'), ('NoCharge', 'No Charge')], max_length=50, null=True))]