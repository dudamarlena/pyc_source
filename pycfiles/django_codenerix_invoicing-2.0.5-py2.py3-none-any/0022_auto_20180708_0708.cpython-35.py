# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/www.django/searchwally/codenerix_invoicing/migrations/0022_auto_20180708_0708.py
# Compiled at: 2018-07-08 01:08:06
# Size of source mod 2**32: 624 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('codenerix_invoicing', '0021_auto_20180523_1036')]
    operations = [
     migrations.AlterField(model_name='salesorder', name='status_order', field=models.CharField(choices=[('PE', 'Pending'), ('PA', 'Payment accepted'), ('SE', 'Sent'), ('DE', 'Delivered'), ('CA', 'Cancelled')], default='PE', max_length=2, verbose_name='Status'))]