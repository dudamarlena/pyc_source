# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ioo/Projets/Django-billjobs/django-billjobs/billjobs/migrations/0008_auto_20180308_1312.py
# Compiled at: 2018-03-08 10:12:13
# Size of source mod 2**32: 571 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('billjobs', '0007_change_service_description_field_max_len')]
    operations = [
     migrations.AlterField(model_name='bill',
       name='number',
       field=models.CharField(blank=True, help_text='This value is set automatically.', max_length=16, unique=True, verbose_name='Bill number'))]