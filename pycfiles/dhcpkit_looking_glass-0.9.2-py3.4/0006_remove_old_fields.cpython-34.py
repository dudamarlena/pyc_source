# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/dhcpkit_looking_glass/migrations/0006_remove_old_fields.py
# Compiled at: 2016-07-18 16:58:03
# Size of source mod 2**32: 2601 bytes
from __future__ import unicode_literals
import django.db.models.deletion
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('dhcpkit_looking_glass', '0005_move_data')]
    operations = [
     migrations.AlterModelOptions(name='transaction', options={'ordering': ('-request_ts', ),  'verbose_name': 'transaction', 
      'verbose_name_plural': 'transactions'}),
     migrations.RenameField(model_name='transaction', old_name='last_request_ll', new_name='request_ll'),
     migrations.RenameField(model_name='transaction', old_name='last_request', new_name='request'),
     migrations.RenameField(model_name='transaction', old_name='last_request_ts', new_name='request_ts'),
     migrations.RenameField(model_name='transaction', old_name='last_request_type', new_name='request_type'),
     migrations.RenameField(model_name='transaction', old_name='last_response', new_name='response'),
     migrations.RenameField(model_name='transaction', old_name='last_response_ts', new_name='response_ts'),
     migrations.RenameField(model_name='transaction', old_name='last_response_type', new_name='response_type'),
     migrations.AlterField(model_name='transaction', name='client', field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dhcpkit_looking_glass.Client')),
     migrations.AlterField(model_name='transaction', name='server', field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dhcpkit_looking_glass.Server')),
     migrations.RemoveField(model_name='transaction', name='duid'),
     migrations.RemoveField(model_name='transaction', name='interface_id'),
     migrations.RemoveField(model_name='transaction', name='remote_id'),
     migrations.AlterUniqueTogether(name='transaction', unique_together={
      ('client', 'server', 'request_ts')})]