# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/sam/git/Kanban/django-autotask/djautotask/migrations/0052_contract_status.py
# Compiled at: 2020-03-20 18:10:32
# Size of source mod 2**32: 445 bytes
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('djautotask', '0051_contract')]
    operations = [
     migrations.AddField(model_name='contract', name='status', field=models.CharField(blank=True, choices=[(0, 'Inactive'), (1, 'Active')], max_length=20, null=True))]