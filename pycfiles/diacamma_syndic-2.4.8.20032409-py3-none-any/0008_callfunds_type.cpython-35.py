# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /var/lib/jenkins/jobs/Diacamma_generic/workspace/syndic/diacamma/condominium/migrations/0008_callfunds_type.py
# Compiled at: 2020-03-20 14:11:00
# Size of source mod 2**32: 696 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('condominium', '0007_callfunds_supporting')]
    operations = [
     migrations.AddField(model_name='callfunds', name='type_call', field=models.IntegerField(choices=[(0, 'current'), (1, 'exceptional'), (2, 'cash advance'),
      (3, 'borrowing'), (4, 'fund for works')], db_index=True, default=0, verbose_name='type of call'))]