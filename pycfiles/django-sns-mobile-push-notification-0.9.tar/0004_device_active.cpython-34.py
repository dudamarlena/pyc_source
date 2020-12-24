# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/rvaziri/django_mobile_push/sns_notification/migrations/0004_device_active.py
# Compiled at: 2018-04-27 15:41:30
# Size of source mod 2**32: 395 bytes
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('sns_notification', '0003_auto_20180427_1801')]
    operations = [
     migrations.AddField(model_name='device', name='active', field=models.BooleanField(default=True))]