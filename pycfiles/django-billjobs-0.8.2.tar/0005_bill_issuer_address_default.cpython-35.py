# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ioo/dev/django-billjobs/billjobs/migrations/0005_bill_issuer_address_default.py
# Compiled at: 2016-03-22 05:48:15
# Size of source mod 2**32: 540 bytes
from __future__ import unicode_literals
from django.db import migrations, models
from billjobs.settings import BILLJOBS_BILL_ISSUER

class Migration(migrations.Migration):
    dependencies = [
     ('billjobs', '0004_auto_20160321_1256')]
    operations = [
     migrations.AlterField(model_name='bill', name='issuer_address', field=models.CharField(default=BILLJOBS_BILL_ISSUER, max_length=1024))]