# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/nodeconductor_paas_oracle/migrations/0003_auto_20160808_0900.py
# Compiled at: 2016-12-16 07:39:01
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('nodeconductor_paas_oracle', '0002_ovm_iaas_support')]
    operations = [
     migrations.AlterField(model_name=b'deployment', name=b'db_name', field=models.CharField(max_length=256, blank=True))]