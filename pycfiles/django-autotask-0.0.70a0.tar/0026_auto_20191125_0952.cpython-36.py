# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/cameron/Dev/kanban-dev/django-autotask/djautotask/migrations/0026_auto_20191125_0952.py
# Compiled at: 2019-11-26 15:02:19
# Size of source mod 2**32: 366 bytes
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
     ('djautotask', '0025_auto_20191125_0939')]
    operations = [
     migrations.AlterModelOptions(name='priority',
       options={'verbose_name_plural': 'Priorities'})]