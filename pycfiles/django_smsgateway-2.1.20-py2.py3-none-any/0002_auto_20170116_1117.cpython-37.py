# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/tim/unleashed/django-smsgateway/smsgateway/migrations/0002_auto_20170116_1117.py
# Compiled at: 2019-04-19 04:31:39
# Size of source mod 2**32: 525 bytes
from __future__ import unicode_literals
from __future__ import absolute_import
from django.db import models, migrations

class Migration(migrations.Migration):
    dependencies = [
     ('smsgateway', '0001_initial')]
    operations = [
     migrations.AlterField(model_name='sms',
       name='gateway_ref',
       field=models.CharField(help_text='A reference id for the gateway', max_length=64, verbose_name='gateway reference', blank=True))]