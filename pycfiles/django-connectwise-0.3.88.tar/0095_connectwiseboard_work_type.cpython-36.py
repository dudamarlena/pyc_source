# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/cameron/Dev/kanban-dev/django-connectwise/djconnectwise/migrations/0095_connectwiseboard_work_type.py
# Compiled at: 2019-07-18 14:57:10
# Size of source mod 2**32: 526 bytes
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('djconnectwise', '0094_connectwiseboard_work_role')]
    operations = [
     migrations.AddField(model_name='connectwiseboard',
       name='work_type',
       field=models.ForeignKey(blank=True, null=True, on_delete=(django.db.models.deletion.SET_NULL), to='djconnectwise.WorkType'))]