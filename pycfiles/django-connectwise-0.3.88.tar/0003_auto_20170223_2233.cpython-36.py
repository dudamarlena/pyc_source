# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/cameron/Dev/kanban-dev/django-connectwise/djconnectwise/migrations/0003_auto_20170223_2233.py
# Compiled at: 2019-05-14 12:25:52
# Size of source mod 2**32: 409 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('djconnectwise', '0002_auto_20170223_2143')]
    operations = [
     migrations.AlterModelOptions(name='boardstatus',
       options={'ordering': ('board__name', 'sort_order', 'name')})]