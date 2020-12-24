# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/sam/git/Kanban/django-autotask/djautotask/migrations/0060_auto_20200414_1522.py
# Compiled at: 2020-05-08 13:23:41
# Size of source mod 2**32: 850 bytes
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('djautotask', '0059_auto_20200414_1242')]
    operations = [
     migrations.AlterField(model_name='servicecall', name='canceled_by_resource', field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='cancelled_service_calls', to='djautotask.Resource')),
     migrations.AlterField(model_name='servicecall', name='creator_resource', field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_service_calls', to='djautotask.Resource'))]