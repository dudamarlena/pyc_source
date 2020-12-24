# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/cameron/Dev/kanban-dev/django-connectwise/djconnectwise/migrations/0061_auto_20180605_1208.py
# Compiled at: 2019-05-14 12:25:52
# Size of source mod 2**32: 385 bytes
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
     ('djconnectwise', '0060_auto_20180605_0840')]
    operations = [
     migrations.AlterModelOptions(name='team',
       options={'ordering':('name', 'id'), 
      'verbose_name_plural':'Teams'})]