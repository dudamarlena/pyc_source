# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/daniel/GitHub/django_sendgrid_repo/django_sendgrid_parse/migrations/0006_auto_20160816_2123.py
# Compiled at: 2016-08-21 23:09:38
# Size of source mod 2**32: 635 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('django_sendgrid_parse', '0005_auto_20160816_1919')]
    operations = [
     migrations.AlterField(model_name='email', name='from_mailbox', field=models.TextField(verbose_name='From')),
     migrations.AlterField(model_name='email', name='to_mailbox', field=models.TextField(verbose_name='To'))]