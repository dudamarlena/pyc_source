# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /var/lib/jenkins/jobs/Diacamma_generic/workspace/asso/diacamma/event/migrations/0004_event_status.py
# Compiled at: 2020-03-20 14:11:02
# Size of source mod 2**32: 528 bytes
from __future__ import unicode_literals
from django.db import migrations
import django_fsm

class Migration(migrations.Migration):
    dependencies = [
     ('event', '0003_bill')]
    operations = [
     migrations.AlterField(model_name='event', name='status', field=django_fsm.FSMIntegerField(choices=[(0, 'building'), (1, 'valid')], db_index=True, default=0, verbose_name='status'))]