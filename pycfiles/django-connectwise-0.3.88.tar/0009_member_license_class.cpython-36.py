# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/cameron/Dev/kanban-dev/django-connectwise/djconnectwise/migrations/0009_member_license_class.py
# Compiled at: 2019-05-14 12:25:52
# Size of source mod 2**32: 507 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('djconnectwise', '0008_project_status_name')]
    operations = [
     migrations.AddField(model_name='member',
       name='license_class',
       field=models.CharField(choices=[('F', 'Full license'), ('A', 'API license')], db_index=True, blank=True, max_length=20, null=True))]