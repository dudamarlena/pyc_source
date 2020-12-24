# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/polona/Olaii/Olaii_Mangopayments/olaii-mangopay/mangopayments/migrations/0001_initial.py
# Compiled at: 2017-09-14 03:16:06
from __future__ import unicode_literals
from django.db import migrations, models
import localflavor.generic.models, django.contrib.postgres.fields.jsonb
from decimal import Decimal
import django_countries.fields, django_filepicker.models
from django.conf import settings

class Migration(migrations.Migration):
    dependencies = [
     migrations.swappable_dependency(settings.AUTH_USER_MODEL)]
    operations = [
     migrations.CreateModel(name=b'MangoPayBankAccount', fields=[
      (
       b'id', models.AutoField(verbose_name=b'ID', serialize=False, auto_created=True, primary_key=True)),
      (
       b'mangopay_id', models.PositiveIntegerField(null=True, blank=True)),
      (
       b'address', models.CharField(default=b'', max_length=254)),
      (
       b'city', models.CharField(default=b'', max_length=255)),
      (
       b'postal_code', models.IntegerField(default=0)),
      (
       b'region', models.CharField(max_length=255, null=True, blank=True)),
      (
       b'country_code', models.CharField(default=b'', max_length=255)),
      (
       b'account_type', models.CharField(default=b'BI', max_length=2, choices=[('BI', 'BIC & IBAN'), ('US', 'Local US Format'), ('O', 'Other')])),
      (
       b'iban', localflavor.generic.models.IBANField(max_length=34, null=True, blank=True)),
      (
       b'bic', localflavor.generic.models.BICField(max_length=11, null=True, blank=True)),
      (
       b'account_number', models.CharField(max_length=15, null=True, blank=True)),
      (
       b'aba', models.CharField(max_length=9, null=True, blank=True)),
      (
       b'deposit_account_type', models.CharField(blank=True, max_length=8, null=True, choices=[('CHECKING', 'Checking'), ('SAVINGS', 'Savings')]))]),
     migrations.CreateModel(name=b'MangoPayCard', fields=[
      (
       b'id', models.AutoField(verbose_name=b'ID', serialize=False, auto_created=True, primary_key=True)),
      (
       b'mangopay_id', models.PositiveIntegerField(null=True, blank=True)),
      (
       b'expiration_date', models.CharField(max_length=4, null=True, blank=True)),
      (
       b'alias', models.CharField(max_length=16, null=True, blank=True)),
      (
       b'provider', models.CharField(max_length=255, null=True, blank=True)),
      (
       b'type', models.CharField(max_length=255, null=True, blank=True)),
      (
       b'is_active', models.BooleanField(default=False)),
      (
       b'is_valid', models.NullBooleanField()),
      (
       b'deleted', models.BooleanField(default=False)),
      (
       b'user', models.ForeignKey(related_name=b'mangopay_cards', to=settings.AUTH_USER_MODEL))]),
     migrations.CreateModel(name=b'MangoPayCardRegistration', fields=[
      (
       b'id', models.AutoField(verbose_name=b'ID', serialize=False, auto_created=True, primary_key=True)),
      (
       b'mangopay_id', models.PositiveIntegerField(null=True, blank=True)),
      (
       b'mangopay_card', models.OneToOneField(related_name=b'mangopay_card_registration', null=True, blank=True, to=b'mangopayments.MangoPayCard'))]),
     migrations.CreateModel(name=b'MangoPayDocument', fields=[
      (
       b'id', models.AutoField(verbose_name=b'ID', serialize=False, auto_created=True, primary_key=True)),
      (
       b'mangopay_id', models.PositiveIntegerField(null=True, blank=True)),
      (
       b'type', models.CharField(max_length=2, choices=[('IP', 'IDENTITY_PROOF'), ('RP', 'REGISTRATION_PROOF'), ('AA', 'ARTICLES_OF_ASSOCIATION'), ('SD', 'SHAREHOLDER_DECLARATION'), ('AP', 'ADDRESS_PROOF')])),
      (
       b'status', models.CharField(blank=True, max_length=1, null=True, choices=[('C', 'CREATED'), ('A', 'VALIDATION_ASKED'), ('V', 'VALIDATED'), ('R', 'REFUSED')])),
      (
       b'refused_reason_message', models.CharField(max_length=255, null=True, blank=True))]),
     migrations.CreateModel(name=b'MangoPayPage', fields=[
      (
       b'id', models.AutoField(verbose_name=b'ID', serialize=False, auto_created=True, primary_key=True)),
      (
       b'file', django_filepicker.models.FPUrlField(max_length=255)),
      (
       b'document', models.ForeignKey(related_name=b'mangopay_pages', to=b'mangopayments.MangoPayDocument'))]),
     migrations.CreateModel(name=b'MangoPayPayIn', fields=[
      (
       b'id', models.AutoField(verbose_name=b'ID', serialize=False, auto_created=True, primary_key=True)),
      (
       b'mangopay_id', models.PositiveIntegerField(null=True, blank=True)),
      (
       b'execution_date', models.DateTimeField(null=True, blank=True)),
      (
       b'status', models.CharField(blank=True, max_length=9, null=True, choices=[('CREATED', 'The request is created but not processed.'), ('SUCCEEDED', 'The request has been successfully processed.'), ('FAILED', 'The request has failed.')])),
      (
       b'debited_funds', models.DecimalField(default=Decimal(b'0.0'), max_digits=12, decimal_places=2)),
      (
       b'fees', models.DecimalField(default=Decimal(b'0.0'), max_digits=12, decimal_places=2)),
      (
       b'currency', models.CharField(default=b'EUR', max_length=255)),
      (
       b'result_code', models.CharField(max_length=6, null=True, blank=True)),
      (
       b'type', models.CharField(max_length=10, choices=[('bank-wire', 'Pay in by BankWire'), ('card-web', 'Pay in by card via web')])),
      (
       b'secure_mode_redirect_url', models.URLField(null=True, blank=True)),
      (
       b'wire_reference', models.CharField(max_length=50, null=True, blank=True)),
      (
       b'mangopay_bank_account', django.contrib.postgres.fields.jsonb.JSONField(null=True, blank=True)),
      (
       b'mangopay_card', models.ForeignKey(related_name=b'mangopay_payins', blank=True, to=b'mangopayments.MangoPayCard', null=True))]),
     migrations.CreateModel(name=b'MangoPayPayOut', fields=[
      (
       b'id', models.AutoField(verbose_name=b'ID', serialize=False, auto_created=True, primary_key=True)),
      (
       b'mangopay_id', models.PositiveIntegerField(null=True, blank=True)),
      (
       b'execution_date', models.DateTimeField(null=True, blank=True)),
      (
       b'status', models.CharField(blank=True, max_length=9, null=True, choices=[('CREATED', 'The request is created but not processed.'), ('SUCCEEDED', 'The request has been successfully processed.'), ('FAILED', 'The request has failed.')])),
      (
       b'debited_funds', models.DecimalField(default=Decimal(b'0.0'), max_digits=12, decimal_places=2)),
      (
       b'fees', models.DecimalField(default=Decimal(b'0.0'), max_digits=12, decimal_places=2)),
      (
       b'currency', models.CharField(default=b'EUR', max_length=255)),
      (
       b'mangopay_bank_account', models.ForeignKey(related_name=b'mangopay_payouts', to=b'mangopayments.MangoPayBankAccount'))]),
     migrations.CreateModel(name=b'MangoPayRefund', fields=[
      (
       b'id', models.AutoField(verbose_name=b'ID', serialize=False, auto_created=True, primary_key=True)),
      (
       b'mangopay_id', models.PositiveIntegerField(null=True, blank=True)),
      (
       b'execution_date', models.DateTimeField(null=True, blank=True)),
      (
       b'status', models.CharField(blank=True, max_length=9, null=True, choices=[('CREATED', 'The request is created but not processed.'), ('SUCCEEDED', 'The request has been successfully processed.'), ('FAILED', 'The request has failed.')])),
      (
       b'result_code', models.CharField(max_length=6, null=True, blank=True)),
      (
       b'mangopay_pay_in', models.ForeignKey(related_name=b'mangopay_refunds', to=b'mangopayments.MangoPayPayIn'))]),
     migrations.CreateModel(name=b'MangoPayTransfer', fields=[
      (
       b'id', models.AutoField(verbose_name=b'ID', serialize=False, auto_created=True, primary_key=True)),
      (
       b'mangopay_id', models.PositiveIntegerField(null=True, blank=True)),
      (
       b'debited_funds', models.DecimalField(default=Decimal(b'0.0'), max_digits=12, decimal_places=2)),
      (
       b'fees', models.DecimalField(default=Decimal(b'0.0'), max_digits=12, decimal_places=2)),
      (
       b'currency', models.CharField(default=b'EUR', max_length=255)),
      (
       b'execution_date', models.DateTimeField(null=True, blank=True)),
      (
       b'status', models.CharField(blank=True, max_length=9, null=True, choices=[('CREATED', 'The request is created but not processed.'), ('SUCCEEDED', 'The request has been successfully processed.'), ('FAILED', 'The request has failed.')])),
      (
       b'result_code', models.CharField(max_length=6, null=True, blank=True))]),
     migrations.CreateModel(name=b'MangoPayUser', fields=[
      (
       b'id', models.AutoField(verbose_name=b'ID', serialize=False, auto_created=True, primary_key=True)),
      (
       b'create_timestamp', models.DateTimeField(auto_now_add=True, null=True)),
      (
       b'last_edit_timestamp', models.DateTimeField(auto_now=True, null=True)),
      (
       b'mangopay_id', models.PositiveIntegerField(null=True, blank=True)),
      (
       b'type', models.CharField(max_length=1, null=True, choices=[('N', 'Natural User'), ('B', 'BUSINESS'), ('O', 'ORGANIZATION')])),
      (
       b'first_name', models.CharField(max_length=99, null=True, blank=True)),
      (
       b'last_name', models.CharField(max_length=99, null=True, blank=True)),
      (
       b'email', models.EmailField(max_length=254, null=True, blank=True)),
      (
       b'birthday', models.DateField(null=True, blank=True)),
      (
       b'country_of_residence', django_countries.fields.CountryField(max_length=2)),
      (
       b'nationality', django_countries.fields.CountryField(max_length=2)),
      (
       b'address', models.CharField(max_length=254, null=True, blank=True)),
      (
       b'city', models.CharField(max_length=255, null=True, blank=True)),
      (
       b'region', models.CharField(max_length=255, null=True, blank=True)),
      (
       b'postal_code', models.IntegerField(default=0, null=True, blank=True)),
      (
       b'country_code', models.CharField(max_length=255, null=True, blank=True))]),
     migrations.CreateModel(name=b'MangoPayWallet', fields=[
      (
       b'id', models.AutoField(verbose_name=b'ID', serialize=False, auto_created=True, primary_key=True)),
      (
       b'mangopay_id', models.PositiveIntegerField(null=True, blank=True)),
      (
       b'currency', models.CharField(default=b'EUR', max_length=3))]),
     migrations.CreateModel(name=b'MangoPayLegalUser', fields=[
      (
       b'mangopayuser_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to=b'mangopayments.MangoPayUser')),
      (
       b'business_name', models.CharField(max_length=254)),
      (
       b'generic_business_email', models.EmailField(max_length=254)),
      (
       b'headquarters_address', models.CharField(max_length=254, null=True, blank=True)),
      (
       b'headquarters_city', models.CharField(max_length=255, null=True, blank=True)),
      (
       b'headquarters_region', models.CharField(max_length=255, null=True, blank=True)),
      (
       b'headquarters_postal_code', models.IntegerField(default=0, null=True, blank=True)),
      (
       b'headquarters_country_code', models.CharField(max_length=255, null=True, blank=True))], bases=('mangopayments.mangopayuser', )),
     migrations.CreateModel(name=b'MangoPayNaturalUser', fields=[
      (
       b'mangopayuser_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to=b'mangopayments.MangoPayUser')),
      (
       b'occupation', models.CharField(max_length=254, null=True, blank=True)),
      (
       b'income_range', models.SmallIntegerField(blank=True, null=True, choices=[(1, '0 - 1,500'), (2, '1,500 - 2,499'), (3, '2,500 - 3,999'), (4, '4,000 - 7,499'), (5, '7,500 - 9,999'), (6, '10,000 +')]))], bases=('mangopayments.mangopayuser', )),
     migrations.AddField(model_name=b'mangopaywallet', name=b'mangopay_user', field=models.ForeignKey(related_name=b'mangopay_wallets', to=b'mangopayments.MangoPayUser')),
     migrations.AddField(model_name=b'mangopayuser', name=b'user', field=models.ForeignKey(related_name=b'mangopay_users', to=settings.AUTH_USER_MODEL)),
     migrations.AddField(model_name=b'mangopaytransfer', name=b'mangopay_credited_wallet', field=models.ForeignKey(related_name=b'mangopay_credited_wallets', to=b'mangopayments.MangoPayWallet')),
     migrations.AddField(model_name=b'mangopaytransfer', name=b'mangopay_debited_wallet', field=models.ForeignKey(related_name=b'mangopay_debited_wallets', to=b'mangopayments.MangoPayWallet')),
     migrations.AddField(model_name=b'mangopayrefund', name=b'mangopay_user', field=models.ForeignKey(related_name=b'mangopay_refunds', to=b'mangopayments.MangoPayUser')),
     migrations.AddField(model_name=b'mangopaypayout', name=b'mangopay_user', field=models.ForeignKey(related_name=b'mangopay_payouts', to=b'mangopayments.MangoPayUser')),
     migrations.AddField(model_name=b'mangopaypayout', name=b'mangopay_wallet', field=models.ForeignKey(related_name=b'mangopay_payouts', to=b'mangopayments.MangoPayWallet')),
     migrations.AddField(model_name=b'mangopaypayin', name=b'mangopay_user', field=models.ForeignKey(related_name=b'mangopay_payins', to=b'mangopayments.MangoPayUser')),
     migrations.AddField(model_name=b'mangopaypayin', name=b'mangopay_wallet', field=models.ForeignKey(related_name=b'mangopay_payins', to=b'mangopayments.MangoPayWallet')),
     migrations.AddField(model_name=b'mangopaydocument', name=b'mangopay_user', field=models.ForeignKey(related_name=b'mangopay_documents', to=b'mangopayments.MangoPayUser')),
     migrations.AddField(model_name=b'mangopaycardregistration', name=b'mangopay_user', field=models.ForeignKey(related_name=b'mangopay_card_registrations', to=b'mangopayments.MangoPayUser')),
     migrations.AddField(model_name=b'mangopaybankaccount', name=b'mangopay_user', field=models.ForeignKey(related_name=b'mangopay_bank_accounts', to=b'mangopayments.MangoPayUser')),
     migrations.CreateModel(name=b'MangoPayPayInBankWire', fields=[], options={b'proxy': True}, bases=('mangopayments.mangopaypayin', )),
     migrations.CreateModel(name=b'MangoPayPayInByCard', fields=[], options={b'proxy': True}, bases=('mangopayments.mangopaypayin', ))]