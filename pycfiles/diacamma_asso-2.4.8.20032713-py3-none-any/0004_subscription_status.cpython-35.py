# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /var/lib/jenkins/jobs/Diacamma_generic/workspace/asso/diacamma/member/migrations/0004_subscription_status.py
# Compiled at: 2020-03-20 14:11:02
# Size of source mod 2**32: 936 bytes
from __future__ import unicode_literals
from django.db import migrations
import django_fsm
from django.db.models.fields.related import ForeignKey
from django.db.models import deletion

class Migration(migrations.Migration):
    dependencies = [
     ('member', '0003_change_permission')]
    operations = [
     migrations.AlterField(model_name='subscription', name='bill', field=ForeignKey(default=None, null=True, on_delete=deletion.SET_NULL, to='invoice.Bill', verbose_name='bill')),
     migrations.AddField(model_name='subscription', name='status', field=django_fsm.FSMIntegerField(choices=[
      (0, 'waiting'), (1, 'building'), (2, 'valid'), (3, 'cancel'), (4, 'disbarred')], db_index=True, default=2, verbose_name='status'))]