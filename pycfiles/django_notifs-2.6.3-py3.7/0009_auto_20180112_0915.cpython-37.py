# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/notifications/migrations/0009_auto_20180112_0915.py
# Compiled at: 2019-02-21 19:34:58
# Size of source mod 2**32: 573 bytes
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('notifications', '0008_notification_extra_data')]
    operations = [
     migrations.AlterField(model_name='notification',
       name='recipient',
       field=models.ForeignKey(null=True, on_delete=(django.db.models.deletion.CASCADE), related_name='notifications', to=(settings.AUTH_USER_MODEL)))]