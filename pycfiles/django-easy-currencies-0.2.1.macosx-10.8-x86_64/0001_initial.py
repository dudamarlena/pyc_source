# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/davidezanotti/PycharmProjects/buythatgame.com/src/django_easy_currencies/migrations/0001_initial.py
# Compiled at: 2014-10-16 05:01:46
from __future__ import unicode_literals
from django.db import models, migrations
import django.core.validators

class Migration(migrations.Migration):
    dependencies = []
    operations = [
     migrations.CreateModel(name=b'Currency', fields=[
      (
       b'code',
       models.CharField(primary_key=True, serialize=False, max_length=3, validators=[
        django.core.validators.MinLengthValidator(3),
        django.core.validators.MaxLengthValidator(3)], help_text=b'Currency code in ISO 4217 format ($ == USD)', db_index=True))], options={b'db_table': b'django_easy_currencies_currency', 
        b'verbose_name': b'Currency', 
        b'verbose_name_plural': b'Currencies'}, bases=(
      models.Model,)),
     migrations.CreateModel(name=b'CurrencyRate', fields=[
      (
       b'id', models.AutoField(verbose_name=b'ID', serialize=False, auto_created=True, primary_key=True)),
      (
       b'target_currency',
       models.CharField(db_index=True, max_length=3, editable=False, validators=[
        django.core.validators.MinLengthValidator(3),
        django.core.validators.MaxLengthValidator(3)])),
      (
       b'rate', models.FloatField()),
      (
       b'original_currency', models.ForeignKey(related_name=b'rates', to=b'django_easy_currencies.Currency'))], options={b'db_table': b'django_easy_currencies_rate', 
        b'verbose_name': b'Currency rate', 
        b'verbose_name_plural': b'Currency rates'}, bases=(
      models.Model,)),
     migrations.AlterUniqueTogether(name=b'currencyrate', unique_together=set([('original_currency', 'target_currency')]))]