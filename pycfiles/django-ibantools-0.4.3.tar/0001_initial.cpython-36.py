# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/contmp/Repositories/world/django-ibantools/ibantools/migrations/0001_initial.py
# Compiled at: 2017-06-05 09:07:47
# Size of source mod 2**32: 3114 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
     migrations.CreateModel(name='BankCodeDE',
       fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'bank_code', models.CharField(max_length=8, verbose_name='Bank code')),
      (
       'payment_service_provider', models.CharField(choices=[(b'1', 'Yes'), (b'2', 'No')], default=b'2', help_text='Merkmal, ob bankleitzahlführender Zahlungsdienstleister („1“) oder nicht („2“)', max_length=1, verbose_name='Payment service provider')),
      (
       'description', models.CharField(help_text='Bezeichnung des Zahlungsdienstleisters (ohne Rechtsform)', max_length=58, verbose_name='Description')),
      (
       'zip_code', models.CharField(max_length=5, verbose_name='Zip code')),
      (
       'city', models.CharField(max_length=35, verbose_name='City')),
      (
       'short_description', models.CharField(help_text=b'Kurzbezeichnung des Zahlungsdienstleisters mit Ort (ohne Rechtsform)', max_length=27, verbose_name='Short description')),
      (
       'pan', models.CharField(help_text='Institutsnummer für PAN', max_length=5, verbose_name='PAN')),
      (
       'bic', models.CharField(help_text='Business Identifier Code', max_length=11, verbose_name='BIC')),
      (
       'check_digit_method', models.CharField(help_text='Kennzeichen für Prüfzifferberechnungsmethode', max_length=2, verbose_name='Check digit method')),
      (
       'dataset_number', models.CharField(help_text='Nummer des Datensatzes', max_length=6, verbose_name='Dataset number')),
      (
       'indicator_changed', models.CharField(choices=[(b'A', 'New'), (b'D', 'Deleted'), (b'M', 'Changed'), (b'U', 'Unchanged')], default=b'A', help_text='Änderungskennzeichen „A“ (Addition) für neue, „D“ (Deletion) für gelöschte, „U“(Unchanged) für unveränderte und „M“ (Modified) für veränderte Datensätze', max_length=1, verbose_name='Indicator changed')),
      (
       'indicator_deleted', models.CharField(choices=[(b'0', 'No declaration'), (b'1', 'Declarted for deletion')], default=b'0', help_text='Hinweis auf eine beabsichtigte Bankleitzahllöschung', max_length=1, verbose_name='Indicator deleted')),
      (
       'succession_bank_code', models.CharField(help_text='Hinweis auf Nachfolge-Bankleitzahl', max_length=8, verbose_name='Succession bank code')),
      (
       'iban_rule', models.CharField(help_text='Kennzeichen für die IBAN-Regel', max_length=6, verbose_name='IBAN Rule'))],
       options={'ordering':('bank_code', ), 
      'verbose_name':'German Bank Code', 
      'verbose_name_plural':'German Bank Codes'})]