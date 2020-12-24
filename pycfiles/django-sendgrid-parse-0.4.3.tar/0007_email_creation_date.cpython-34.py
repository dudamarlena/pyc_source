# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/daniel/GitHub/django_sendgrid_repo/django_sendgrid_parse/migrations/0007_email_creation_date.py
# Compiled at: 2016-09-09 23:49:09
# Size of source mod 2**32: 605 bytes
from __future__ import unicode_literals
from django.db import migrations, models
import django.utils.timezone

class Migration(migrations.Migration):
    dependencies = [
     ('django_sendgrid_parse', '0006_auto_20160816_2123')]
    operations = [
     migrations.AddField(model_name='email', name='creation_date', field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='Creation date'), preserve_default=False)]