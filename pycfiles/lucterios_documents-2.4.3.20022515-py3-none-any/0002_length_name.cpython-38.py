# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /var/lib/jenkins/jobs/Lucterios_Standard/workspace/lct-documents/lucterios/documents/migrations/0002_length_name.py
# Compiled at: 2019-10-15 08:48:27
# Size of source mod 2**32: 636 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('documents', '0001_initial')]
    operations = [
     migrations.AlterField(model_name='document',
       name='name',
       field=models.CharField(max_length=250, verbose_name='name')),
     migrations.AlterField(model_name='folder',
       name='name',
       field=models.CharField(max_length=250, verbose_name='name'))]