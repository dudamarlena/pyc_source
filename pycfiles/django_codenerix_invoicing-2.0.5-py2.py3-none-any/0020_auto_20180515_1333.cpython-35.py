# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/www.django/erp.juanmitaboada.com/codenerix_invoicing/migrations/0020_auto_20180515_1333.py
# Compiled at: 2018-05-24 09:19:04
# Size of source mod 2**32: 856 bytes
from __future__ import unicode_literals
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
     ('codenerix_invoicing', '0019_auto_20180515_1235')]
    operations = [
     migrations.RemoveField(model_name='saleslines', name='discounts'),
     migrations.RemoveField(model_name='saleslines', name='equivalence_surcharges'),
     migrations.RemoveField(model_name='saleslines', name='subtotal'),
     migrations.RemoveField(model_name='saleslines', name='taxes'),
     migrations.RemoveField(model_name='saleslines', name='total')]