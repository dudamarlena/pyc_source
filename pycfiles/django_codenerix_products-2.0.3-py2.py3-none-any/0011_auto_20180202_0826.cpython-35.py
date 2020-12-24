# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/www.django/makarthy/codenerix_products/migrations/0011_auto_20180202_0826.py
# Compiled at: 2018-02-05 00:32:32
# Size of source mod 2**32: 424 bytes
from __future__ import unicode_literals
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
     ('codenerix_products', '0010_merge_20180202_0726')]
    operations = [
     migrations.AlterUniqueTogether(name='productunique', unique_together=set([]))]