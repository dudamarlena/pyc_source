# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /var/lib/jenkins/jobs/Lucterios_Standard/workspace/lct-core/lucterios/CORE/migrations/0003_printmodel_mode.py
# Compiled at: 2020-03-26 06:35:14
# Size of source mod 2**32: 456 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('CORE', '0002_savedcriteria')]
    operations = [
     migrations.AddField(model_name='printmodel',
       name='mode',
       field=models.IntegerField(verbose_name='mode', default=0, choices=[(0, 'Simple'), (1, 'Advanced')]))]