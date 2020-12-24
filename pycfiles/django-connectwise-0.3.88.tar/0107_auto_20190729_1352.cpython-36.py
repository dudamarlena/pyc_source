# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/cameron/Dev/kanban-dev/django-connectwise/djconnectwise/migrations/0107_auto_20190729_1352.py
# Compiled at: 2019-08-14 13:00:26
# Size of source mod 2**32: 1172 bytes
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('djconnectwise', '0106_auto_20190722_1524')]
    operations = [
     migrations.AddField(model_name='connectwiseboard',
       name='bill_time',
       field=models.CharField(blank=True, choices=[('Billable', 'Billable'), ('DoNotBill', 'Do Not Bill'), ('NoCharge', 'No Charge')], max_length=50, null=True)),
     migrations.AddField(model_name='member',
       name='work_role',
       field=models.ForeignKey(null=True, on_delete=(django.db.models.deletion.SET_NULL), to='djconnectwise.WorkRole')),
     migrations.AddField(model_name='member',
       name='work_type',
       field=models.ForeignKey(null=True, on_delete=(django.db.models.deletion.SET_NULL), to='djconnectwise.WorkType')),
     migrations.AddField(model_name='worktype',
       name='overall_default_flag',
       field=models.BooleanField(default=False))]