# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/cameron/Dev/kanban-dev/django-connectwise/djconnectwise/migrations/0012_auto_20170320_1057.py
# Compiled at: 2019-05-14 12:25:52
# Size of source mod 2**32: 584 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('djconnectwise', '0011_company_deleted_flag')]
    operations = [
     migrations.AddField(model_name='ticket',
       name='has_child_ticket',
       field=(models.NullBooleanField())),
     migrations.AddField(model_name='ticket',
       name='parent_ticket_id',
       field=models.IntegerField(blank=True, null=True))]