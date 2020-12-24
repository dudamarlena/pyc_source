# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/notifications/migrations/0008_notification_extra_data.py
# Compiled at: 2019-02-21 19:34:58
# Size of source mod 2**32: 429 bytes
from django.db import migrations
import notifications.fields

class Migration(migrations.Migration):
    dependencies = [
     ('notifications', '0007_auto_20171006_0126')]
    operations = [
     migrations.AddField(model_name='notification',
       name='extra_data',
       field=notifications.fields.JSONField(default={}))]