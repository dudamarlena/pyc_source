# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/sam/git/Kanban/django-autotask/djautotask/migrations/0055_auto_20200325_0928.py
# Compiled at: 2020-05-08 13:23:41
# Size of source mod 2**32: 740 bytes
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('djautotask', '0054_merge_20200323_1511')]
    operations = [
     migrations.AddField(model_name='project', name='contract', field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='djautotask.Contract')),
     migrations.AddField(model_name='ticket', name='contract', field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='djautotask.Contract'))]