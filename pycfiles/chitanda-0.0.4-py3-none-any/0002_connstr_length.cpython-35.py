# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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