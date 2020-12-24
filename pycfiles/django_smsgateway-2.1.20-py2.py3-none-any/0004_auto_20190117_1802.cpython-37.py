# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/tim/unleashed/django-smsgateway/smsgateway/migrations/0004_auto_20190117_1802.py
# Compiled at: 2019-04-19 04:31:39
# Size of source mod 2**32: 437 bytes
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('smsgateway', '0003_auto_20171012_1427')]
    operations = [
     migrations.AlterField(model_name='queuedsms',
       name='reliable',
       field=models.BooleanField(blank=True, default=False, verbose_name='is reliable'))]