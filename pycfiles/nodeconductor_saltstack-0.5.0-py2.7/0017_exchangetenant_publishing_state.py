# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/nodeconductor_saltstack/exchange/migrations/0017_exchangetenant_publishing_state.py
# Compiled at: 2016-09-28 02:05:53
from __future__ import unicode_literals
from django.db import models, migrations

class Migration(migrations.Migration):
    dependencies = [
     ('exchange', '0016_remove_mailbox_size')]
    operations = [
     migrations.AddField(model_name=b'exchangetenant', name=b'publishing_state', field=models.CharField(default=b'not published', max_length=30, choices=[('not published', 'Not published'), ('published', 'Published'), ('requested', 'Requested')]), preserve_default=True)]