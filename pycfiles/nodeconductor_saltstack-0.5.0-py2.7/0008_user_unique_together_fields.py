# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/nodeconductor_saltstack/exchange/migrations/0008_user_unique_together_fields.py
# Compiled at: 2016-09-28 02:05:53
from __future__ import unicode_literals
from django.db import models, migrations

class Migration(migrations.Migration):
    dependencies = [
     ('exchange', '0007_user_additional_fields')]
    operations = [
     migrations.AlterField(model_name=b'user', name=b'username', field=models.CharField(max_length=255), preserve_default=True),
     migrations.AlterUniqueTogether(name=b'user', unique_together=set([('name', 'tenant'), ('username', 'tenant')]))]