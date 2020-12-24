# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/sam/git/Kanban/django-autotask/djautotask/migrations/0002_ticket_ticket_number.py
# Compiled at: 2019-10-01 19:08:49
# Size of source mod 2**32: 407 bytes
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('djautotask', '0001_initial')]
    operations = [
     migrations.AddField(model_name='ticket', name='ticket_number', field=models.CharField(blank=True, max_length=50, null=True))]