# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/cameron/Dev/kanban-dev/django-connectwise/djconnectwise/migrations/0080_auto_20181210_0930.py
# Compiled at: 2019-05-14 12:25:52
# Size of source mod 2**32: 404 bytes
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('djconnectwise', '0079_auto_20181203_1606')]
    operations = [
     migrations.AlterField(model_name='member',
       name='last_name',
       field=models.CharField(max_length=30, null=True))]