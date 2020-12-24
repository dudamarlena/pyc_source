# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/rvaziri/django_mobile_push/sns_notification/migrations/0002_auto_20180427_1758.py
# Compiled at: 2018-04-27 13:58:05
# Size of source mod 2**32: 718 bytes
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
     ('sns_notification', '0001_initial')]
    operations = [
     migrations.RemoveField(model_name='device', name='active'),
     migrations.RemoveField(model_name='device', name='language'),
     migrations.RemoveField(model_name='device', name='last_active_at'),
     migrations.RemoveField(model_name='device', name='version'),
     migrations.DeleteModel(name='language')]