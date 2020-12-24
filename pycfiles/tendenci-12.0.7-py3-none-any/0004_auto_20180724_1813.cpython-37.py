# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jennyq/.pyenv/versions/venv_t12/lib/python3.7/site-packages/tendenci/apps/payments/stripe/migrations/0004_auto_20180724_1813.py
# Compiled at: 2020-03-30 17:48:04
# Size of source mod 2**32: 1326 bytes
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('stripe', '0003_charge')]
    operations = [
     migrations.AlterField(model_name='stripeaccount',
       name='account_name',
       field=models.CharField(default='', max_length=250)),
     migrations.AlterField(model_name='stripeaccount',
       name='country',
       field=models.CharField(default='US', max_length=5)),
     migrations.AlterField(model_name='stripeaccount',
       name='default_currency',
       field=models.CharField(default='usd', max_length=5)),
     migrations.AlterField(model_name='stripeaccount',
       name='email',
       field=models.CharField(default='', max_length=200)),
     migrations.AlterField(model_name='stripeaccount',
       name='status',
       field=models.BooleanField(default=True, verbose_name='Active')),
     migrations.AlterField(model_name='stripeaccount',
       name='status_detail',
       field=models.CharField(default='active', max_length=50))]