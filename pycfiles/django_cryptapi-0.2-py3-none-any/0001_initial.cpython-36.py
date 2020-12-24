# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /mnt/c/Users/dwjor/Google Drive/Code/Python/django-cryptapi/cryptapi/migrations/0001_initial.py
# Compiled at: 2020-05-04 20:02:30
# Size of source mod 2**32: 4439 bytes
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
     migrations.CreateModel(name='Payment',
       fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'value_paid', models.DecimalField(decimal_places=0, default=0, max_digits=65, verbose_name='Value Paid')),
      (
       'value_received', models.DecimalField(decimal_places=0, default=0, max_digits=65, verbose_name='Value Received')),
      (
       'txid_in', models.CharField(default='', max_length=256, verbose_name='TXID in')),
      (
       'txid_out', models.CharField(default='', max_length=256, verbose_name='TXID out')),
      (
       'confirmations', models.IntegerField(default=0)),
      (
       'timestamp', models.DateTimeField(auto_now_add=True))]),
     migrations.CreateModel(name='PaymentLog',
       fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'raw_data', models.CharField(max_length=8192)),
      (
       'timestamp', models.DateTimeField(auto_now_add=True)),
      (
       'payment', models.ForeignKey(null=True, on_delete=(django.db.models.deletion.SET_NULL), to='cryptapi.Payment'))]),
     migrations.CreateModel(name='Provider',
       fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'coin', models.CharField(choices=[('btc', 'Bitcoin'), ('eth', 'Ethereum'), ('bch', 'Bitcoin Cash'), ('ltc', 'Litecoin'), ('iota', 'IOTA')], max_length=8, unique=True, verbose_name='Coin')),
      (
       'cold_wallet', models.CharField(max_length=128, verbose_name='Cold Wallet')),
      (
       'active', models.BooleanField(default=True, verbose_name='Active'))]),
     migrations.CreateModel(name='Request',
       fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'order_id', models.CharField(default='', max_length=128, verbose_name='Order ID')),
      (
       'nonce', models.CharField(default='', max_length=32, unique=True, verbose_name='Nonce')),
      (
       'address_in', models.CharField(default='', max_length=128, null=True, verbose_name='Payment Address')),
      (
       'address_out', models.CharField(default='', max_length=128, null=True, verbose_name='Receiving Address')),
      (
       'value_requested', models.DecimalField(decimal_places=0, default=0, max_digits=65, verbose_name='Value Requested')),
      (
       'status', models.CharField(choices=[('created', 'Created'), ('insufficient', 'Payment Insufficient'), ('received', 'Received'), ('done', 'Done')], default='', max_length=16, null=True, verbose_name='Status')),
      (
       'raw_request_url', models.CharField(default='', max_length=8192, null=True, verbose_name='Request URL')),
      (
       'timestamp', models.DateTimeField(auto_now_add=True)),
      (
       'provider', models.ForeignKey(null=True, on_delete=(django.db.models.deletion.SET_NULL), to='cryptapi.Provider'))]),
     migrations.CreateModel(name='RequestLog',
       fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'raw_data', models.CharField(max_length=8192)),
      (
       'timestamp', models.DateTimeField(auto_now_add=True)),
      (
       'request', models.ForeignKey(null=True, on_delete=(django.db.models.deletion.SET_NULL), to='cryptapi.Request'))]),
     migrations.AddField(model_name='payment',
       name='request',
       field=models.ForeignKey(null=True, on_delete=(django.db.models.deletion.SET_NULL), to='cryptapi.Request')),
     migrations.AlterUniqueTogether(name='request',
       unique_together={
      ('provider', 'order_id')})]