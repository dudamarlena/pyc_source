# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/monobot/sync/tickettest/simpletickets/migrations/0003_auto_20150830_2321.py
# Compiled at: 2015-08-30 19:21:10
from __future__ import unicode_literals
from django.db import models, migrations

class Migration(migrations.Migration):
    dependencies = [
     ('simpletickets', '0002_auto_20150830_2241')]
    operations = [
     migrations.AlterField(model_name=b'ticket', name=b'state', field=models.IntegerField(default=1, choices=[(1, 'new'), (2, 'assigned'), (5, 'delayed'), (8, 'solved'), (9, 'closed')]))]