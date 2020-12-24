# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /var/lib/jenkins/jobs/Lucterios_Standard/workspace/lct-contacts/lucterios/mailing/migrations/0009_message_message_type.py
# Compiled at: 2020-04-23 13:50:26
# Size of source mod 2**32: 463 bytes
from django.db import migrations
import django_fsm

class Migration(migrations.Migration):
    dependencies = [
     ('mailing', '0008_documentcontainer')]
    operations = [
     migrations.AddField(model_name='message',
       name='message_type',
       field=django_fsm.FSMIntegerField(choices=[(0, 'email'), (1, 'sms')], default=0, verbose_name='type'))]