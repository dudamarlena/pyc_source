# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/nodeconductor_saltstack/exchange/migrations/0010_group_members.py
# Compiled at: 2016-09-28 02:05:53
from __future__ import unicode_literals
from django.db import models, migrations

class Migration(migrations.Migration):
    dependencies = [
     ('exchange', '0009_user_username_validation')]
    operations = [
     migrations.AddField(model_name=b'group', name=b'members', field=models.ManyToManyField(to=b'exchange.User'), preserve_default=True),
     migrations.AlterField(model_name=b'user', name=b'username', field=models.CharField(max_length=255), preserve_default=True)]