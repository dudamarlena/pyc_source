# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/www.django/makarthy/codenerix_email/migrations/0006_emailmessage_error.py
# Compiled at: 2017-11-16 12:01:16
# Size of source mod 2**32: 489 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('codenerix_email', '0005_emailmessage_retries')]
    operations = [
     migrations.AddField(model_name='emailmessage', name='error', field=models.BooleanField(default=False, verbose_name='Error'))]