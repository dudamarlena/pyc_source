# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/cameron/Dev/kanban-dev/django-autotask/djautotask/migrations/0017_auto_20191021_1028.py
# Compiled at: 2019-11-22 18:06:23
# Size of source mod 2**32: 1423 bytes
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
     ('djautotask', '0016_auto_20191021_0958')]
    operations = [
     migrations.AlterModelManagers(name='displaycolor',
       managers=[]),
     migrations.AlterModelManagers(name='issuetype',
       managers=[]),
     migrations.AlterModelManagers(name='projectstatus',
       managers=[]),
     migrations.AlterModelManagers(name='projecttype',
       managers=[]),
     migrations.AlterModelManagers(name='queue',
       managers=[]),
     migrations.AlterModelManagers(name='source',
       managers=[]),
     migrations.AlterModelManagers(name='subissuetype',
       managers=[]),
     migrations.AlterModelManagers(name='ticketpriority',
       managers=[]),
     migrations.AlterModelManagers(name='ticketstatus',
       managers=[]),
     migrations.AlterModelManagers(name='tickettype',
       managers=[])]