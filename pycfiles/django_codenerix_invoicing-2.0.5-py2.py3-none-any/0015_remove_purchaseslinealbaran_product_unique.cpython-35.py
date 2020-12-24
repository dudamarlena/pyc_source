# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/www.django/makarthy/codenerix_invoicing/migrations/0015_remove_purchaseslinealbaran_product_unique.py
# Compiled at: 2018-02-27 03:00:28
# Size of source mod 2**32: 427 bytes
from __future__ import unicode_literals
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
     ('codenerix_invoicing', '0014_auto_20180227_0858')]
    operations = [
     migrations.RemoveField(model_name='purchaseslinealbaran', name='product_unique')]