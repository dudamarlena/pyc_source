# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /mnt/c/django-danceschool/currentmaster/django-danceschool/danceschool/financial/migrations/0008_revenueitem_buyerpayssalestax.py
# Compiled at: 2018-03-26 19:55:30
# Size of source mod 2**32: 507 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('financial', '0007_auto_20170823_1047')]
    operations = [
     migrations.AddField(model_name='revenueitem', name='buyerPaysSalesTax', field=models.BooleanField(default=False, verbose_name='Buyer pays sales tax'))]