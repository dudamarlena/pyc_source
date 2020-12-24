# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/nodeconductor_saltstack/exchange/migrations/0006_group_manager_foreign_key.py
# Compiled at: 2016-09-28 02:05:53
from __future__ import unicode_literals
from django.db import models, migrations

class Migration(migrations.Migration):
    dependencies = [
     ('exchange', '0005_contact_group_user')]
    operations = [
     migrations.RemoveField(model_name=b'group', name=b'manager_email'),
     migrations.AddField(model_name=b'group', name=b'manager', field=models.ForeignKey(related_name=b'groups', default=1, to=b'exchange.User'), preserve_default=False)]