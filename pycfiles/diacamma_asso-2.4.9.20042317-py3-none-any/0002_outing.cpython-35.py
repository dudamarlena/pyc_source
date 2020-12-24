# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /var/lib/jenkins/jobs/Diacamma_generic/workspace/asso/diacamma/event/migrations/0002_outing.py
# Compiled at: 2020-03-20 14:11:02
# Size of source mod 2**32: 885 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('event', '0001_initial')]
    operations = [
     migrations.AlterModelOptions(name='event', options={'ordering': ['-date'], 'verbose_name': 'event', 'verbose_name_plural': 'events'}),
     migrations.AddField(model_name='event', name='date_end', field=models.DateField(null=True, verbose_name='end date')),
     migrations.AddField(model_name='event', name='event_type', field=models.IntegerField(choices=[(0, 'examination'), (1, 'trainning/outing')], db_index=True, default=0, verbose_name='event type'))]