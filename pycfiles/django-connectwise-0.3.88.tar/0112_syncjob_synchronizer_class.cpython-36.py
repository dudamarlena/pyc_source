# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/cameron/Dev/kanban-dev/django-connectwise/djconnectwise/migrations/0112_syncjob_synchronizer_class.py
# Compiled at: 2020-01-06 15:58:00
# Size of source mod 2**32: 428 bytes
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('djconnectwise', '0111_auto_20191204_0838')]
    operations = [
     migrations.AddField(model_name='syncjob',
       name='synchronizer_class',
       field=models.CharField(blank=True, max_length=100, null=True))]