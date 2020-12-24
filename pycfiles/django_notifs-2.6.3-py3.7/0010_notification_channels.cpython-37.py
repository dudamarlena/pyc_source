# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/notifications/migrations/0010_notification_channels.py
# Compiled at: 2019-02-21 19:34:58
# Size of source mod 2**32: 491 bytes
from django.db import migrations
import notifications.fields

class Migration(migrations.Migration):
    dependencies = [
     ('notifications', '0009_auto_20180112_0915')]
    operations = [
     migrations.AddField(model_name='notification',
       name='channels',
       field=notifications.fields.ListField(default=('console', ), max_length=200),
       preserve_default=False)]