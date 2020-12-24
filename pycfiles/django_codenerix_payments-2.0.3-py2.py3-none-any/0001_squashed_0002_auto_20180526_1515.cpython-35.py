# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/www.django/erp.juanmitaboada.com/codenerix_payments/migrations/0001_squashed_0002_auto_20180526_1515.py
# Compiled at: 2018-05-26 09:18:55
# Size of source mod 2**32: 7247 bytes
from __future__ import unicode_literals
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion

def setup(apps, schema_editor):
    Currency = apps.get_model('codenerix_payments', 'Currency')
    currency = Currency()
    currency.name = 'Euro'
    currency.symbol = '€'.encode('utf-8')
    currency.iso4217 = 'EUR'
    currency.price = 1.0
    currency.save()


class Migration(migrations.Migration):
    replaces = [
     ('codenerix_payments', '0001_initial'), ('codenerix_payments', '0002_auto_20180526_1515')]
    initial = True
    dependencies = []
    operations = [
     migrations.CreateModel(name='Currency', fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
      (
       'updated', models.DateTimeField(auto_now=True, verbose_name='Updated')),
      (
       'name', models.CharField(max_length=15, unique=True, verbose_name='Name')),
      (
       'symbol', models.CharField(max_length=2, unique=True, verbose_name='Symbol')),
      (
       'iso4217', models.CharField(max_length=3, unique=True, verbose_name='ISO 4217 Code')),
      (
       'price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Price'))], options={'default_permissions': ('add', 'change', 'delete', 'view', 'list'), 
      'abstract': False}),
     migrations.CreateModel(name='PaymentAnswer', fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
      (
       'updated', models.DateTimeField(auto_now=True, verbose_name='Updated')),
      (
       'ref', models.CharField(default=None, max_length=50, null=True, verbose_name='Reference')),
      (
       'error', models.BooleanField(default=False, verbose_name='Error')),
      (
       'error_txt', models.TextField(blank=True, null=True, verbose_name='Error Text')),
      (
       'request', models.TextField(blank=True, null=True, verbose_name='Request')),
      (
       'answer', models.TextField(blank=True, null=True, verbose_name='Answer')),
      (
       'request_date', models.DateTimeField(blank=True, editable=False, null=True, verbose_name='Request date')),
      (
       'answer_date', models.DateTimeField(blank=True, editable=False, null=True, verbose_name='Answer date'))], options={'default_permissions': ('add', 'change', 'delete', 'view', 'list'), 
      'abstract': False}),
     migrations.CreateModel(name='PaymentConfirmation', fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
      (
       'updated', models.DateTimeField(auto_now=True, verbose_name='Updated')),
      (
       'ref', models.CharField(default=None, max_length=50, null=True, verbose_name='Reference')),
      (
       'action', models.CharField(choices=[('confirm', 'Confirm'), ('cancel', 'Cancel')], max_length=7, verbose_name='Action')),
      (
       'data', models.TextField(blank=True, null=True, verbose_name='Data')),
      (
       'error', models.BooleanField(default=False, verbose_name='Error')),
      (
       'error_txt', models.TextField(blank=True, null=True, verbose_name='Error Text'))], options={'default_permissions': ('add', 'change', 'delete', 'view', 'list'), 
      'abstract': False}),
     migrations.CreateModel(name='PaymentRequest', fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
      (
       'updated', models.DateTimeField(auto_now=True, verbose_name='Updated')),
      (
       'locator', models.CharField(max_length=40, unique=True, verbose_name='Locator')),
      (
       'ref', models.CharField(default=None, max_length=50, null=True, verbose_name='Reference')),
      (
       'order', models.PositiveIntegerField(validators=[django.core.validators.MaxValueValidator(2821109907455)], verbose_name='Order Reference')),
      (
       'reverse', models.CharField(max_length=64, verbose_name='Reverse')),
      (
       'platform', models.CharField(max_length=20, verbose_name='Platform')),
      (
       'protocol', models.CharField(choices=[('paypal', 'Paypal'), ('redsys', 'Redsys'), ('redsysxml', 'Redsys XML')], max_length=10, verbose_name='Protocol')),
      (
       'real', models.BooleanField(default=False, verbose_name='Real')),
      (
       'error', models.BooleanField(default=False, verbose_name='Error')),
      (
       'error_txt', models.TextField(blank=True, null=True, verbose_name='Error Text')),
      (
       'cancelled', models.BooleanField(default=False, verbose_name='Cancelled')),
      (
       'total', models.FloatField(verbose_name='Total')),
      (
       'notes', models.CharField(blank=True, max_length=30, null=True, verbose_name='Notes')),
      (
       'request', models.TextField(blank=True, null=True, verbose_name='Request')),
      (
       'answer', models.TextField(blank=True, null=True, verbose_name='Answer')),
      (
       'request_date', models.DateTimeField(blank=True, editable=False, null=True, verbose_name='Request date')),
      (
       'answer_date', models.DateTimeField(blank=True, editable=False, null=True, verbose_name='Answer date')),
      (
       'currency', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payments', to='codenerix_payments.Currency'))], options={'default_permissions': ('add', 'change', 'delete', 'view', 'list'), 
      'abstract': False}),
     migrations.AddField(model_name='paymentconfirmation', name='payment', field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='paymentconfirmations', to='codenerix_payments.PaymentRequest')),
     migrations.AddField(model_name='paymentanswer', name='payment', field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='paymentanswers', to='codenerix_payments.PaymentRequest')),
     migrations.AlterField(model_name='currency', name='symbol', field=models.CharField(max_length=5, unique=True, verbose_name='Symbol')),
     migrations.RunPython(setup)]