# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ioo/Projets/Django-billjobs/django-billjobs/billjobs/migrations/0007_change_service_description_field_max_len.py
# Compiled at: 2017-04-12 02:08:09
# Size of source mod 2**32: 569 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('billjobs', '0006_add_billin_address_and_migrate_data')]
    operations = [
     migrations.AlterField(model_name='service',
       name='description',
       field=models.CharField(help_text='Write service description limited to 256 characters', max_length=256, verbose_name='Description'))]