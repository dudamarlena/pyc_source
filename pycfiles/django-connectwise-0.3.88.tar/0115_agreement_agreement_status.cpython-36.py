# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/cameron/Dev/kanban-dev/django-connectwise/djconnectwise/migrations/0115_agreement_agreement_status.py
# Compiled at: 2020-04-16 16:15:52
# Size of source mod 2**32: 427 bytes
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('djconnectwise', '0114_auto_20200219_1515')]
    operations = [
     migrations.AddField(model_name='agreement',
       name='agreement_status',
       field=models.CharField(blank=True, max_length=50, null=True))]