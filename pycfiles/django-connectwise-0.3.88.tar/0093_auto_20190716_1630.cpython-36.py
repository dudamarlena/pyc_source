# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/cameron/Dev/kanban-dev/django-connectwise/djconnectwise/migrations/0093_auto_20190716_1630.py
# Compiled at: 2019-07-18 16:22:29
# Size of source mod 2**32: 611 bytes
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('djconnectwise', '0092_remove_ticket_work_type')]
    operations = [
     migrations.AddField(model_name='ticket',
       name='automatic_email_cc',
       field=models.CharField(blank=True, max_length=1000, null=True)),
     migrations.AddField(model_name='timeentry',
       name='email_cc',
       field=models.CharField(blank=True, max_length=1000, null=True))]