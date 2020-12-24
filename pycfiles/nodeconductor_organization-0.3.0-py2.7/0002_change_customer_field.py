# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/nodeconductor_organization/migrations/0002_change_customer_field.py
# Compiled at: 2016-09-25 10:50:25
from __future__ import unicode_literals
from django.db import models, migrations
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('nodeconductor_organization', '0001_initial')]
    operations = [
     migrations.AlterField(model_name=b'organization', name=b'customer', field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, blank=True, to=b'structure.Customer'), preserve_default=True)]