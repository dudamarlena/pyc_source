# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/sam/git/Kanban/django-autotask/djautotask/migrations/0064_auto_20200511_1124.py
# Compiled at: 2020-05-12 14:51:19
# Size of source mod 2**32: 1330 bytes
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('djautotask', '0063_accountphysicallocation')]
    operations = [
     migrations.AddField(model_name='ticket', name='first_response_date_time', field=models.DateTimeField(blank=True, null=True)),
     migrations.AddField(model_name='ticket', name='first_response_due_date_time', field=models.DateTimeField(blank=True, null=True)),
     migrations.AddField(model_name='ticket', name='resolution_plan_date_time', field=models.DateTimeField(blank=True, null=True)),
     migrations.AddField(model_name='ticket', name='resolution_plan_due_date_time', field=models.DateTimeField(blank=True, null=True)),
     migrations.AddField(model_name='ticket', name='resolved_date_time', field=models.DateTimeField(blank=True, null=True)),
     migrations.AddField(model_name='ticket', name='resolved_due_date_time', field=models.DateTimeField(blank=True, null=True))]