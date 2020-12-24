# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/cameron/Dev/kanban-dev/django-connectwise/djconnectwise/migrations/0104_auto_20190722_1232.py
# Compiled at: 2019-08-14 13:00:26
# Size of source mod 2**32: 411 bytes
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
     ('djconnectwise', '0103_activitystatus_activitytype')]
    operations = [
     migrations.AlterModelOptions(name='activitystatus',
       options={'ordering':('name', ), 
      'verbose_name_plural':'activity statuses'})]