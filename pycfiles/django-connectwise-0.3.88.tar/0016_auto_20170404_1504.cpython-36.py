# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/cameron/Dev/kanban-dev/django-connectwise/djconnectwise/migrations/0016_auto_20170404_1504.py
# Compiled at: 2019-05-14 12:25:52
# Size of source mod 2**32: 453 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('djconnectwise', '0015_auto_20170404_1504')]
    operations = [
     migrations.AlterField(model_name='companystatus',
       name='notification_message',
       field=models.CharField(max_length=500, null=True, blank=True))]