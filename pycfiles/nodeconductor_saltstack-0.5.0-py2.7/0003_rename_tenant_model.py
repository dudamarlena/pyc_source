# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/nodeconductor_saltstack/exchange/migrations/0003_rename_tenant_model.py
# Compiled at: 2016-09-28 02:05:53
from __future__ import unicode_literals
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
     ('taggit', '0002_auto_20150616_2121'),
     ('saltstack', '0001_initial'),
     ('exchange', '0002_tenant_tags')]
    operations = [
     migrations.RenameModel(old_name=b'Tenant', new_name=b'ExchangeTenant')]