# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ioo/Projets/Django-billjobs/django-billjobs/billjobs/migrations/0007_service_account_number.py
# Compiled at: 2016-11-27 07:23:08
# Size of source mod 2**32: 539 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('billjobs', '0006_add_billin_address_and_migrate_data')]
    operations = [
     migrations.AddField(model_name='service', name='account_number', field=models.PositiveIntegerField(blank=True, null=True, unique=True, verbose_name='Account number'))]