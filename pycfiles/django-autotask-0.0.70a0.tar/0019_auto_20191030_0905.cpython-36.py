# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/cameron/Dev/kanban-dev/django-autotask/djautotask/migrations/0019_auto_20191030_0905.py
# Compiled at: 2019-11-01 15:21:24
# Size of source mod 2**32: 451 bytes
from django.db import migrations
import django.db.models.manager

class Migration(migrations.Migration):
    dependencies = [
     ('djautotask', '0018_auto_20191029_1634')]
    operations = [
     migrations.AlterModelManagers(name='resource',
       managers=[
      (
       'regular_objects', django.db.models.manager.Manager())])]