# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/cameron/Dev/kanban-dev/django-connectwise/djconnectwise/migrations/0072_remove_callbackentry_member.py
# Compiled at: 2019-05-14 12:25:52
# Size of source mod 2**32: 339 bytes
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
     ('djconnectwise', '0071_auto_20180822_1300')]
    operations = [
     migrations.RemoveField(model_name='callbackentry',
       name='member')]