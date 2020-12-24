# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/dhcpkit_looking_glass/migrations/0005_move_data.py
# Compiled at: 2016-07-18 18:16:22
# Size of source mod 2**32: 1648 bytes
from __future__ import unicode_literals
from django.db import migrations

def fill_servers(apps, schema_editor):
    server_model = apps.get_model('dhcpkit_looking_glass', 'Server')
    transaction_model = apps.get_model('dhcpkit_looking_glass', 'Transaction')
    server, created = server_model.objects.get_or_create(name='Unknown')
    for transaction in transaction_model.objects.filter(server=None):
        transaction.server = server
        transaction.save()


def fill_clients(apps, schema_editor):
    client_model = apps.get_model('dhcpkit_looking_glass', 'Client')
    transaction_model = apps.get_model('dhcpkit_looking_glass', 'Transaction')
    for transaction in transaction_model.objects.filter(client=None):
        client, created = client_model.objects.get_or_create(duid=transaction.duid, interface_id=transaction.interface_id, remote_id=transaction.remote_id)
        transaction.client = client
        transaction.save()


class Migration(migrations.Migration):
    dependencies = [
     ('dhcpkit_looking_glass', '0004_add_client_server')]
    operations = [
     migrations.RunPython(fill_servers),
     migrations.RunPython(fill_clients)]