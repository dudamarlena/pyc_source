# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/contmp/Repositories/world/django-ibantools/ibantools/migrations/0001_initial.py
# Compiled at: 2017-06-05 09:07:47
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
     migrations.CreateModel(name=b'BankCodeDE', fields=[
      (
       b'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name=b'ID')),
      (
       b'bank_code', models.CharField(max_length=8, verbose_name=b'Bank code')),
      (
       b'payment_service_provider', models.CharField(choices=[('1', 'Yes'), ('2', 'No')], default=b'2', help_text=b'Merkmal, ob bankleitzahlführender Zahlungsdienstleister („1“) oder nicht („2“)', max_length=1, verbose_name=b'Payment service provider')),
      (
       b'description', models.CharField(help_text=b'Bezeichnung des Zahlungsdienstleisters (ohne Rechtsform)', max_length=58, verbose_name=b'Description')),
      (
       b'zip_code', models.CharField(max_length=5, verbose_name=b'Zip code')),
      (
       b'city', models.CharField(max_length=35, verbose_name=b'City')),
      (
       b'short_description', models.CharField(help_text=b'Kurzbezeichnung des Zahlungsdienstleisters mit Ort (ohne Rechtsform)', max_length=27, verbose_name=b'Short description')),
      (
       b'pan', models.CharField(help_text=b'Institutsnummer für PAN', max_length=5, verbose_name=b'PAN')),
      (
       b'bic', models.CharField(help_text=b'Business Identifier Code', max_length=11, verbose_name=b'BIC')),
      (
       b'check_digit_method', models.CharField(help_text=b'Kennzeichen für Prüfzifferberechnungsmethode', max_length=2, verbose_name=b'Check digit method')),
      (
       b'dataset_number', models.CharField(help_text=b'Nummer des Datensatzes', max_length=6, verbose_name=b'Dataset number')),
      (
       b'indicator_changed', models.CharField(choices=[('A', 'New'), ('D', 'Deleted'), ('M', 'Changed'), ('U', 'Unchanged')], default=b'A', help_text=b'Änderungskennzeichen „A“ (Addition) für neue, „D“ (Deletion) für gelöschte, „U“(Unchanged) für unveränderte und „M“ (Modified) für veränderte Datensätze', max_length=1, verbose_name=b'Indicator changed')),
      (
       b'indicator_deleted', models.CharField(choices=[('0', 'No declaration'), ('1', 'Declarted for deletion')], default=b'0', help_text=b'Hinweis auf eine beabsichtigte Bankleitzahllöschung', max_length=1, verbose_name=b'Indicator deleted')),
      (
       b'succession_bank_code', models.CharField(help_text=b'Hinweis auf Nachfolge-Bankleitzahl', max_length=8, verbose_name=b'Succession bank code')),
      (
       b'iban_rule', models.CharField(help_text=b'Kennzeichen für die IBAN-Regel', max_length=6, verbose_name=b'IBAN Rule'))], options={b'ordering': ('bank_code', ), 
        b'verbose_name': b'German Bank Code', 
        b'verbose_name_plural': b'German Bank Codes'})]