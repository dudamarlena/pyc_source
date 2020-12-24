# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/sam/git/Kanban/django-autotask/djautotask/migrations/0040_auto_20200204_1538.py
# Compiled at: 2020-02-05 12:36:04
# Size of source mod 2**32: 644 bytes
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('djautotask', '0039_merge_20200131_1022')]
    operations = [
     migrations.AlterField(model_name='task', name='estimated_hours', field=models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True)),
     migrations.AlterField(model_name='task', name='remaining_hours', field=models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True))]