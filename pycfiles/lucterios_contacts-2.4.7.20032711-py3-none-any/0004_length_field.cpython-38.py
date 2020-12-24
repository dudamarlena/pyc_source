# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /var/lib/jenkins/jobs/Lucterios_Standard/workspace/lct-contacts/lucterios/contacts/migrations/0004_length_field.py
# Compiled at: 2020-03-26 06:35:18
# Size of source mod 2**32: 1425 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('contacts', '0003_createaccount')]
    operations = [
     migrations.AlterField(model_name='abstractcontact',
       name='tel1',
       field=models.CharField(blank=True, max_length=20, verbose_name='tel1')),
     migrations.AlterField(model_name='abstractcontact',
       name='tel2',
       field=models.CharField(blank=True, max_length=20, verbose_name='tel2')),
     migrations.AlterField(model_name='customfield',
       name='name',
       field=models.CharField(max_length=200, verbose_name='name')),
     migrations.AlterField(model_name='individual',
       name='firstname',
       field=models.CharField(max_length=100, verbose_name='firstname')),
     migrations.AlterField(model_name='individual',
       name='lastname',
       field=models.CharField(max_length=100, verbose_name='lastname')),
     migrations.AlterField(model_name='legalentity',
       name='identify_number',
       field=models.TextField(blank=True, verbose_name='identify number'))]