# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/chisubmit/backend/api/migrations/0002_connstr_length.py
# Compiled at: 2017-04-03 16:34:20
# Size of source mod 2**32: 589 bytes
from __future__ import unicode_literals
from django.db import models, migrations

class Migration(migrations.Migration):
    dependencies = [
     ('api', '0001_initial')]
    operations = [
     migrations.AlterField(model_name='course', name='git_server_connstr', field=models.CharField(max_length=256, null=True)),
     migrations.AlterField(model_name='course', name='git_staging_connstr', field=models.CharField(max_length=256, null=True))]