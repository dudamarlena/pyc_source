# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/rvaziri/django_mobile_push/sns_notification/migrations/0003_auto_20180427_1801.py
# Compiled at: 2018-04-27 14:01:11
# Size of source mod 2**32: 433 bytes
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
     ('sns_notification', '0002_auto_20180427_1758')]
    operations = [
     migrations.RemoveField(model_name='device', name='user'),
     migrations.RemoveField(model_name='log', name='user')]