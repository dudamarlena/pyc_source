# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/tim/unleashed/django-smsgateway/smsgateway/migrations/0003_auto_20171012_1427.py
# Compiled at: 2019-04-19 04:31:39
# Size of source mod 2**32: 755 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('smsgateway', '0002_auto_20170116_1117')]
    operations = [
     migrations.AlterField(model_name='queuedsms',
       name='priority',
       field=models.CharField(choices=[('1', 'high'), ('2', 'medium'), ('3', 'low'), ('9', 'deferred')], default='2', max_length=1)),
     migrations.AlterField(model_name='sms',
       name='backend',
       field=models.CharField(db_index=True, default='unknown', max_length=32, verbose_name='backend'))]