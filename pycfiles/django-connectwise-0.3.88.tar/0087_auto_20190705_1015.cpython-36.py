# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/cameron/Dev/kanban-dev/django-connectwise/djconnectwise/migrations/0087_auto_20190705_1015.py
# Compiled at: 2019-07-10 16:32:12
# Size of source mod 2**32: 1061 bytes
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('djconnectwise', '0086_merge_20190507_1402')]
    operations = [
     migrations.AddField(model_name='ticket',
       name='automatic_email_cc_flag',
       field=models.BooleanField(default=False)),
     migrations.AddField(model_name='ticket',
       name='automatic_email_contact_flag',
       field=models.BooleanField(default=False)),
     migrations.AddField(model_name='ticket',
       name='automatic_email_resource_flag',
       field=models.BooleanField(default=False)),
     migrations.AddField(model_name='ticket',
       name='bill_time',
       field=models.CharField(blank=True, choices=[('Billable', 'Billable'), ('DoNotBill', 'Do Not Bill'), ('NoCharge', 'No Charge'), ('NoDefault', 'No Default')], max_length=20, null=True))]