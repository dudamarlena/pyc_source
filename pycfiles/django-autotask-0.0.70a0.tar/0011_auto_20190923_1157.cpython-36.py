# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/cameron/Dev/kanban-dev/django-autotask/djautotask/migrations/0011_auto_20190923_1157.py
# Compiled at: 2019-09-24 18:25:25
# Size of source mod 2**32: 360 bytes
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
     ('djautotask', '0010_merge_20190923_1155')]
    operations = [
     migrations.AlterModelOptions(name='queue',
       options={'verbose_name_plural': 'Queues'})]