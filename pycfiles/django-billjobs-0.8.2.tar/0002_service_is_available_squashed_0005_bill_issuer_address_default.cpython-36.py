# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ioo/Projets/Django-billjobs/django-billjobs/billjobs/migrations/0002_service_is_available_squashed_0005_bill_issuer_address_default.py
# Compiled at: 2016-03-22 05:48:15
# Size of source mod 2**32: 1157 bytes
from __future__ import unicode_literals
from django.db import migrations, models
from billjobs.settings import BILLJOBS_BILL_ISSUER

class Migration(migrations.Migration):
    replaces = [
     ('billjobs', '0002_service_is_available'), ('billjobs', '0003_billline_note'), ('billjobs', '0004_auto_20160321_1256'), ('billjobs', '0005_bill_issuer_address_default')]
    dependencies = [
     ('billjobs', '0001_initial')]
    operations = [
     migrations.AddField(model_name='service',
       name='is_available',
       field=models.BooleanField(default=True, verbose_name='Is available ?')),
     migrations.AddField(model_name='billline',
       name='note',
       field=models.CharField(blank=True, help_text='Write a simple note which will be added in your bill', max_length=1024, verbose_name='Note')),
     migrations.AddField(model_name='bill',
       name='issuer_address',
       field=models.CharField(default=BILLJOBS_BILL_ISSUER, max_length=1024))]