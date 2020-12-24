# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jennyq/.pyenv/versions/venv_t12/lib/python3.7/site-packages/tendenci/apps/invoices/migrations/0003_auto_20181008_1243.py
# Compiled at: 2020-03-30 17:48:04
# Size of source mod 2**32: 449 bytes
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('invoices', '0002_auto_20160308_1501')]
    operations = [
     migrations.AlterField(model_name='invoice',
       name='variance',
       field=models.DecimalField(decimal_places=2, default=0, max_digits=10))]