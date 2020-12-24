# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/nodeconductor_saltstack/exchange/migrations/0012_more_members_models.py
# Compiled at: 2016-09-28 02:05:53
from __future__ import unicode_literals
from django.db import models, migrations

class Migration(migrations.Migration):
    dependencies = [
     ('exchange', '0011_conferenceroom')]
    operations = [
     migrations.AddField(model_name=b'group', name=b'delivery_members', field=models.ManyToManyField(related_name=b'+', to=b'exchange.User'), preserve_default=True),
     migrations.AddField(model_name=b'group', name=b'senders_out', field=models.BooleanField(default=False, help_text=b'Delivery management for senders outside organizational unit'), preserve_default=True),
     migrations.AddField(model_name=b'user', name=b'send_as_members', field=models.ManyToManyField(related_name=b'send_as_members_rel_+', to=b'exchange.User'), preserve_default=True),
     migrations.AddField(model_name=b'user', name=b'send_on_behalf_members', field=models.ManyToManyField(related_name=b'send_on_behalf_members_rel_+', to=b'exchange.User'), preserve_default=True),
     migrations.AlterField(model_name=b'group', name=b'members', field=models.ManyToManyField(related_name=b'+', to=b'exchange.User'), preserve_default=True)]