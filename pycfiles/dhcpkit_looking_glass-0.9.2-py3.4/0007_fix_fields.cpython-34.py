# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/dhcpkit_looking_glass/migrations/0007_fix_fields.py
# Compiled at: 2016-07-18 16:58:06
# Size of source mod 2**32: 1546 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('dhcpkit_looking_glass', '0006_remove_old_fields')]
    operations = [
     migrations.AlterField(model_name='transaction', name='request', field=models.TextField(blank=True, null=True, verbose_name='request')),
     migrations.AlterField(model_name='transaction', name='request_ts', field=models.DateTimeField(blank=True, null=True, verbose_name='request timestamp')),
     migrations.AlterField(model_name='transaction', name='request_type', field=models.CharField(blank=True, max_length=50, null=True, verbose_name='request type')),
     migrations.AlterField(model_name='transaction', name='response', field=models.TextField(blank=True, null=True, verbose_name='response')),
     migrations.AlterField(model_name='transaction', name='response_ts', field=models.DateTimeField(blank=True, null=True, verbose_name='response timestamp')),
     migrations.AlterField(model_name='transaction', name='response_type', field=models.CharField(blank=True, max_length=50, null=True, verbose_name='response type'))]