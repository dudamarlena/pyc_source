# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/www.django/makarthy/codenerix_email/migrations/0005_emailmessage_retries.py
# Compiled at: 2017-11-16 11:58:08
# Size of source mod 2**32: 495 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('codenerix_email', '0004_auto_20171108_1628')]
    operations = [
     migrations.AddField(model_name='emailmessage', name='retries', field=models.PositiveIntegerField(default=0, verbose_name='Retries'))]