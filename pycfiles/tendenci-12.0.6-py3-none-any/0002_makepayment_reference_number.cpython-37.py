# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jennyq/.pyenv/versions/venv_t12/lib/python3.7/site-packages/tendenci/apps/make_payments/migrations/0002_makepayment_reference_number.py
# Compiled at: 2020-03-30 17:48:04
# Size of source mod 2**32: 395 bytes
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('make_payments', '0001_initial')]
    operations = [
     migrations.AddField(model_name='makepayment',
       name='reference_number',
       field=models.CharField(default='', max_length=20, blank=True))]