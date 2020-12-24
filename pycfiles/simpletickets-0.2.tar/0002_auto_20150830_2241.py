# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/monobot/sync/tickettest/simpletickets/migrations/0002_auto_20150830_2241.py
# Compiled at: 2015-08-30 18:41:37
from __future__ import unicode_literals
from django.db import models, migrations

class Migration(migrations.Migration):
    dependencies = [
     ('simpletickets', '0001_initial')]
    operations = [
     migrations.AlterField(model_name=b'ticket', name=b'state', field=models.CharField(default=b'new', max_length=15, choices=[('new', 'new'), ('assigned', 'assigned'), ('solved', 'solved'), ('closed', 'closed')]))]