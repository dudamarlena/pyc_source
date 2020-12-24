# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/cameron/Dev/kanban-dev/django-connectwise/djconnectwise/migrations/0055_auto_20180501_1022.py
# Compiled at: 2019-05-14 12:25:52
# Size of source mod 2**32: 427 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('djconnectwise', '0054_auto_20180501_1009')]
    operations = [
     migrations.AlterModelOptions(name='servicenote',
       options={'verbose_name_plural':'Notes', 
      'ordering':('-date_created', 'id')})]