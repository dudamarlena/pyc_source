# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/cameron/Dev/kanban-dev/django-connectwise/djconnectwise/migrations/0014_company_status.py
# Compiled at: 2019-05-14 12:25:52
# Size of source mod 2**32: 477 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('djconnectwise', '0013_auto_20170403_1203')]
    operations = [
     migrations.AddField(model_name='company',
       name='status',
       field=models.ForeignKey(blank=True, null=True, to='djconnectwise.CompanyStatus', on_delete=(models.SET_NULL)))]