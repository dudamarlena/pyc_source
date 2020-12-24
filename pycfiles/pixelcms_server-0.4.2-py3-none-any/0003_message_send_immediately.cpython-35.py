# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mw/dev/pixelcms-server/cms/emails/migrations/0003_message_send_immediately.py
# Compiled at: 2017-01-10 18:47:51
# Size of source mod 2**32: 454 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('emails', '0002_massmessage')]
    operations = [
     migrations.AddField(model_name='message', name='send_immediately', field=models.BooleanField(default=True))]