# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dmeliza/Devel/django-neurobank/neurobank/migrations/0004_auto_20170624_0941.py
# Compiled at: 2017-06-24 09:41:22
# Size of source mod 2**32: 535 bytes
from __future__ import unicode_literals
import django.contrib.postgres.fields.hstore
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
     ('neurobank', '0003_auto_20170624_0933')]
    operations = [
     migrations.AlterField(model_name='resource', name='metadata', field=django.contrib.postgres.fields.hstore.HStoreField(blank=True, null=True))]