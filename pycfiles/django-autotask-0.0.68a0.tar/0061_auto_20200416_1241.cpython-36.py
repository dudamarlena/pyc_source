# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/cameron/Dev/kanban-dev/django-autotask/djautotask/migrations/0061_auto_20200416_1241.py
# Compiled at: 2020-04-16 20:47:33
# Size of source mod 2**32: 410 bytes
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
     ('djautotask', '0060_auto_20200414_1522')]
    operations = [
     migrations.AlterModelOptions(name='servicecallstatus',
       options={'ordering':('label', ), 
      'verbose_name_plural':'Service call statuses'})]