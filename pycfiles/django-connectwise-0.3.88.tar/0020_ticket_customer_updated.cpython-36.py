# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/cameron/Dev/kanban-dev/django-connectwise/djconnectwise/migrations/0020_ticket_customer_updated.py
# Compiled at: 2019-05-14 12:25:52
# Size of source mod 2**32: 413 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('djconnectwise', '0019_ticket_owner')]
    operations = [
     migrations.AddField(model_name='ticket',
       name='customer_updated',
       field=models.BooleanField(default=False))]