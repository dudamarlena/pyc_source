# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/www.django/makarthy/codenerix_products/migrations/0008_auto_20180126_1711.py
# Compiled at: 2018-02-02 06:33:32
# Size of source mod 2**32: 527 bytes
from __future__ import unicode_literals
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
     ('codenerix_products', '0007_auto_20180123_1316')]
    operations = [
     migrations.RemoveField(model_name='productfinal', name='stock_lock'),
     migrations.RemoveField(model_name='productfinal', name='stock_real')]