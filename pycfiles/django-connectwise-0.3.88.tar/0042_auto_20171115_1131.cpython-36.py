# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/cameron/Dev/kanban-dev/django-connectwise/djconnectwise/migrations/0042_auto_20171115_1131.py
# Compiled at: 2019-05-14 12:25:52
# Size of source mod 2**32: 461 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('djconnectwise', '0041_auto_20171030_1047')]
    operations = [
     migrations.RemoveField(model_name='ticket',
       name='api_text'),
     migrations.RemoveField(model_name='ticket',
       name='type')]