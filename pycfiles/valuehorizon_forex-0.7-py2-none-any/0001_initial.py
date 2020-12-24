# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/kevin/Development/customapps/valuehorizon-forex/forex/migrations/0001_initial.py
# Compiled at: 2016-06-02 13:23:51
from __future__ import unicode_literals
from django.db import models, migrations

class Migration(migrations.Migration):
    dependencies = []
    operations = [
     migrations.CreateModel(name=b'Currency', fields=[
      (
       b'id', models.AutoField(verbose_name=b'ID', serialize=False, auto_created=True, primary_key=True)),
      (
       b'name', models.CharField(max_length=255)),
      (
       b'symbol', models.CharField(unique=True, max_length=10)),
      (
       b'ascii_symbol', models.CharField(max_length=20, null=True, blank=True)),
      (
       b'num_code', models.IntegerField(null=True, blank=True)),
      (
       b'digits', models.IntegerField(null=True, blank=True)),
      (
       b'description', models.TextField(blank=True)),
      (
       b'latest_date', models.DateField(null=True, editable=False, blank=True)),
      (
       b'latest_ask_price', models.DecimalField(null=True, editable=False, max_digits=20, decimal_places=4, blank=True)),
      (
       b'latest_ask_price_us', models.DecimalField(null=True, editable=False, max_digits=20, decimal_places=4, blank=True)),
      (
       b'latest_change', models.DecimalField(null=True, editable=False, max_digits=20, decimal_places=2, blank=True)),
      (
       b'change_52_week', models.DecimalField(null=True, editable=False, max_digits=20, decimal_places=2, blank=True)),
      (
       b'volatility_52_week', models.DecimalField(null=True, editable=False, max_digits=20, decimal_places=2, blank=True))], options={b'ordering': [
                    b'symbol'], 
        b'verbose_name': b'Currency', 
        b'verbose_name_plural': b'Currencies'}),
     migrations.CreateModel(name=b'CurrencyPrices', fields=[
      (
       b'id', models.AutoField(verbose_name=b'ID', serialize=False, auto_created=True, primary_key=True)),
      (
       b'date', models.DateField()),
      (
       b'ask_price', models.DecimalField(max_digits=20, decimal_places=4)),
      (
       b'bid_price', models.DecimalField(null=True, max_digits=20, decimal_places=4, blank=True)),
      (
       b'ask_price_us', models.DecimalField(null=True, max_digits=20, decimal_places=4, blank=True)),
      (
       b'bid_price_us', models.DecimalField(null=True, max_digits=20, decimal_places=4, blank=True)),
      (
       b'name', models.CharField(max_length=255, null=True, blank=True)),
      (
       b'is_monthly', models.BooleanField(default=False)),
      (
       b'currency', models.ForeignKey(to=b'forex.Currency'))], options={b'ordering': [
                    b'date'], 
        b'get_latest_by': b'date', 
        b'verbose_name': b'Currency Price', 
        b'verbose_name_plural': b'Currency Prices'}),
     migrations.AlterUniqueTogether(name=b'currencyprices', unique_together=set([('date', 'currency')]))]