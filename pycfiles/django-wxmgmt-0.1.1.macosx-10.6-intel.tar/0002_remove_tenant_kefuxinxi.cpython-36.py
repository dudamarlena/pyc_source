# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/lidayan/pyenv/python3/pypi-distribute/lib/python3.6/site-packages/wxmgmt/migrations/0002_remove_tenant_kefuxinxi.py
# Compiled at: 2018-02-25 20:14:49
# Size of source mod 2**32: 319 bytes
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
     ('wxmgmt', '0001_initial')]
    operations = [
     migrations.RemoveField(model_name='tenant',
       name='kefuxinxi')]