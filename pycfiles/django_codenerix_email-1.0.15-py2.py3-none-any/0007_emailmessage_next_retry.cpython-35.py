# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/www.django/makarthy/codenerix_email/migrations/0007_emailmessage_next_retry.py
# Compiled at: 2017-11-16 12:58:28
# Size of source mod 2**32: 602 bytes
from __future__ import unicode_literals
from django.db import migrations, models
import django.utils.timezone

class Migration(migrations.Migration):
    dependencies = [
     ('codenerix_email', '0006_emailmessage_error')]
    operations = [
     migrations.AddField(model_name='emailmessage', name='next_retry', field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='Next retry'), preserve_default=False)]