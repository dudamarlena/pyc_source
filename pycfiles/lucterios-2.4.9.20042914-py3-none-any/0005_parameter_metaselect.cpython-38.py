# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /var/lib/jenkins/jobs/Lucterios_Standard/workspace/lct-core/lucterios/CORE/migrations/0005_parameter_metaselect.py
# Compiled at: 2020-03-26 06:35:14
# Size of source mod 2**32: 474 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('CORE', '0004_printmodel_is_default')]
    operations = [
     migrations.AddField(model_name='parameter',
       name='metaselect',
       field=models.TextField(blank=True, verbose_name='meta'))]