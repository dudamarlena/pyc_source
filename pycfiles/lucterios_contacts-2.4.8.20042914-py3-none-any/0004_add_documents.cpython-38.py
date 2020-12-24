# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /var/lib/jenkins/jobs/Lucterios_Standard/workspace/lct-contacts/lucterios/mailing/migrations/0004_add_documents.py
# Compiled at: 2020-03-26 06:35:18
# Size of source mod 2**32: 733 bytes
from django.db import migrations, models
import django_fsm

class Migration(migrations.Migration):
    dependencies = [
     ('documents', '0002_length_name'),
     ('mailing', '0003_transition')]
    operations = [
     migrations.AddField(model_name='message',
       name='documents',
       field=models.ManyToManyField(blank=True, to='documents.Document', verbose_name='documents')),
     migrations.AlterField(model_name='message',
       name='status',
       field=django_fsm.FSMIntegerField(choices=[(0, 'open'), (1, 'valided'), (2, 'sending')], default=0, verbose_name='status'))]