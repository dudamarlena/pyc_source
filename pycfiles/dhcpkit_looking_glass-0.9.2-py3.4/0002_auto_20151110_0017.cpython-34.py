# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/dhcpkit_looking_glass/migrations/0002_auto_20151110_0017.py
# Compiled at: 2016-07-18 16:24:34
# Size of source mod 2**32: 622 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('dhcpkit_looking_glass', '0001_initial')]
    operations = [
     migrations.AddField(model_name='client', name='last_request_type', field=models.CharField(blank=True, max_length=50, null=True)),
     migrations.AddField(model_name='client', name='last_response_type', field=models.CharField(blank=True, max_length=50, null=True))]