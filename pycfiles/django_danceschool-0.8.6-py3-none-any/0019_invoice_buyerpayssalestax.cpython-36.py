# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /c/Users/Lee/Sync/projects/django-danceschool/currentmaster/django-danceschool/danceschool/core/migrations/0019_invoice_buyerpayssalestax.py
# Compiled at: 2019-04-03 22:56:26
# Size of source mod 2**32: 498 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('core', '0018_auto_20170910_2352')]
    operations = [
     migrations.AddField(model_name='invoice',
       name='buyerPaysSalesTax',
       field=models.BooleanField(default=False, verbose_name='Buyer pays sales tax'))]