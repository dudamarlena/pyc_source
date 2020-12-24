# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /var/lib/jenkins/jobs/Lucterios_Standard/workspace/lct-contacts/lucterios/mailing/migrations/0007_message_statistics.py
# Compiled at: 2020-03-26 06:35:18
# Size of source mod 2**32: 623 bytes
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('mailing', '0006_message_doc_in_link')]
    operations = [
     migrations.AddField(model_name='emailsent',
       name='last_open_date',
       field=models.DateTimeField(default=None, null=True, verbose_name='last open date')),
     migrations.AddField(model_name='emailsent',
       name='nb_open',
       field=models.IntegerField(default=0, verbose_name='number open'))]