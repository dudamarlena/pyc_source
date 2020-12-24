# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/nodeconductor_saltstack/saltstack/migrations/0003_unique_spl.py
# Compiled at: 2016-09-28 02:05:53
from __future__ import unicode_literals
from django.db import models, migrations

class Migration(migrations.Migration):
    dependencies = [
     ('saltstack', '0002_init_exchange_quota')]
    operations = [
     migrations.AlterUniqueTogether(name=b'saltstackserviceprojectlink', unique_together=set([('service', 'project')]))]