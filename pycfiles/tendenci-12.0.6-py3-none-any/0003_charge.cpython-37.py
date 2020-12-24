# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jennyq/.pyenv/versions/venv_t12/lib/python3.7/site-packages/tendenci/apps/payments/stripe/migrations/0003_charge.py
# Compiled at: 2020-02-26 15:07:58
# Size of source mod 2**32: 1347 bytes
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('stripe', '0002_auto_20180508_1659')]
    operations = [
     migrations.CreateModel(name='Charge',
       fields=[
      (
       'id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
      (
       'charge_id', models.CharField(default='', max_length=100)),
      (
       'amount', models.DecimalField(max_digits=15, decimal_places=2)),
      (
       'amount_refunded', models.DecimalField(max_digits=15, decimal_places=2)),
      (
       'currency', models.CharField(default='usd', max_length=5)),
      (
       'captured', models.BooleanField(default=False)),
      (
       'livemode', models.BooleanField(default=False)),
      (
       'charge_dt', models.DateTimeField(verbose_name='Charged On')),
      (
       'create_dt', models.DateTimeField(auto_now_add=True, verbose_name='Created On')),
      (
       'update_dt', models.DateTimeField(auto_now=True, verbose_name='Last Updated')),
      (
       'account', models.ForeignKey(related_name='stripe_charges', to='stripe.StripeAccount', on_delete=(django.db.models.deletion.CASCADE)))])]