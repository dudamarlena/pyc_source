# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/gustavo/Projects/grupobienestar/epayco_django/migrations/0001_initial.py
# Compiled at: 2020-01-20 12:15:56
# Size of source mod 2**32: 4337 bytes
from django.db import migrations, models
import django.utils.timezone, model_utils.fields

class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
     migrations.CreateModel(name='PaymentConfirmation',
       fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'created', model_utils.fields.AutoCreatedField(default=(django.utils.timezone.now), editable=False, verbose_name='created')),
      (
       'modified', model_utils.fields.AutoLastModifiedField(default=(django.utils.timezone.now), editable=False, verbose_name='modified')),
      (
       'flag', models.BooleanField(default=False)),
      (
       'flag_code', models.CharField(choices=[('1001', 'Duplicate Transaction'), ('1002', 'Invalid Sign')], max_length=4)),
      (
       'flag_info', models.CharField(max_length=100)),
      (
       'amount', models.CharField(max_length=32)),
      (
       'amount_country', models.CharField(max_length=32)),
      (
       'amount_ok', models.CharField(max_length=32)),
      (
       'tax', models.CharField(max_length=32)),
      (
       'amount_base', models.CharField(max_length=32)),
      (
       'currency_code', models.CharField(max_length=4)),
      (
       'cardnumber', models.CharField(max_length=32)),
      (
       'quotas', models.PositiveSmallIntegerField()),
      (
       'transaction_id', models.CharField(max_length=16)),
      (
       'transaction_state', models.CharField(max_length=16)),
      (
       'bank_name', models.CharField(max_length=128)),
      (
       'response', models.CharField(max_length=16)),
      (
       'approval_code', models.CharField(max_length=16)),
      (
       'transaction_date', models.CharField(max_length=32)),
      (
       'cod_response', models.CharField(max_length=8)),
      (
       'response_reason_text', models.CharField(max_length=32)),
      (
       'errorcode', models.CharField(max_length=16)),
      (
       'cod_transaction_state', models.CharField(max_length=8)),
      (
       'business', models.CharField(max_length=256)),
      (
       'franchise', models.CharField(max_length=8)),
      (
       'cust_id_cliente', models.CharField(max_length=128)),
      (
       'customer_doctype', models.CharField(max_length=3)),
      (
       'customer_document', models.CharField(max_length=16)),
      (
       'customer_name', models.CharField(max_length=128)),
      (
       'customer_lastname', models.CharField(max_length=128)),
      (
       'customer_email', models.CharField(max_length=128)),
      (
       'customer_phone', models.CharField(max_length=32)),
      (
       'customer_movil', models.CharField(max_length=32)),
      (
       'customer_ind_pais', models.CharField(max_length=32)),
      (
       'customer_country', models.CharField(max_length=32)),
      (
       'customer_city', models.CharField(max_length=32)),
      (
       'customer_address', models.TextField()),
      (
       'customer_ip', models.CharField(max_length=16)),
      (
       'invoice_id', models.CharField(max_length=128)),
      (
       'ref_payco', models.CharField(max_length=128)),
      (
       'signature', models.CharField(max_length=256)),
      (
       'description', models.TextField()),
      (
       'test_request', models.BooleanField()),
      (
       'extra1', models.CharField(max_length=255)),
      (
       'extra2', models.CharField(max_length=255)),
      (
       'extra3', models.CharField(max_length=255)),
      (
       'extra4', models.CharField(max_length=255)),
      (
       'extra5', models.CharField(max_length=255)),
      (
       'extra6', models.CharField(max_length=255)),
      (
       'extra7', models.CharField(max_length=255)),
      (
       'extra8', models.CharField(max_length=255)),
      (
       'extra9', models.CharField(max_length=255)),
      (
       'extra10', models.CharField(max_length=255)),
      (
       'raw', models.TextField())],
       options={'db_table': 'epayco_payment_confirmation'})]