# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/cameron/Dev/kanban-dev/django-connectwise/djconnectwise/migrations/0092_remove_ticket_work_type.py
# Compiled at: 2019-07-16 17:55:55
# Size of source mod 2**32: 335 bytes
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
     ('djconnectwise', '0091_worktype_bill_time')]
    operations = [
     migrations.RemoveField(model_name='ticket',
       name='work_type')]