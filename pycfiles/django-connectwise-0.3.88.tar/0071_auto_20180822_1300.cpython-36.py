# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/cameron/Dev/kanban-dev/django-connectwise/djconnectwise/migrations/0071_auto_20180822_1300.py
# Compiled at: 2019-05-14 12:25:52
# Size of source mod 2**32: 1659 bytes
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('djconnectwise', '0070_mycompanyother')]
    operations = [
     migrations.AlterField(model_name='project',
       name='actual_hours',
       field=models.DecimalField(blank=True, decimal_places=2, max_digits=9, null=True)),
     migrations.AlterField(model_name='project',
       name='budget_hours',
       field=models.DecimalField(blank=True, decimal_places=2, max_digits=9, null=True)),
     migrations.AlterField(model_name='project',
       name='scheduled_hours',
       field=models.DecimalField(blank=True, decimal_places=2, max_digits=9, null=True)),
     migrations.AlterField(model_name='ticket',
       name='actual_hours',
       field=models.DecimalField(blank=True, decimal_places=2, max_digits=9, null=True)),
     migrations.AlterField(model_name='ticket',
       name='budget_hours',
       field=models.DecimalField(blank=True, decimal_places=2, max_digits=9, null=True)),
     migrations.AlterField(model_name='timeentry',
       name='actual_hours',
       field=models.DecimalField(blank=True, decimal_places=2, max_digits=9, null=True)),
     migrations.AlterField(model_name='timeentry',
       name='hours_deduct',
       field=models.DecimalField(blank=True, decimal_places=2, max_digits=9, null=True))]