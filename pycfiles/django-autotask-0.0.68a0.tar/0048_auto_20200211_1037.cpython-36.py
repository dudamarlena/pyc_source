# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/cameron/Dev/kanban-dev/django-autotask/djautotask/migrations/0048_auto_20200211_1037.py
# Compiled at: 2020-02-28 16:41:52
# Size of source mod 2**32: 853 bytes
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('djautotask', '0047_auto_20200207_1126')]
    operations = [
     migrations.AlterField(model_name='timeentry',
       name='hours_to_bill',
       field=models.DecimalField(blank=True, decimal_places=4, max_digits=9, null=True)),
     migrations.AlterField(model_name='timeentry',
       name='hours_worked',
       field=models.DecimalField(blank=True, decimal_places=4, max_digits=9, null=True)),
     migrations.AlterField(model_name='timeentry',
       name='offset_hours',
       field=models.DecimalField(blank=True, decimal_places=4, max_digits=9, null=True))]