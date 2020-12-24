# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dana/.virtualenvs/django-cryptographic-fields/lib/python2.7/site-packages/testapp/migrations/0001_initial.py
# Compiled at: 2015-05-01 13:43:24
from __future__ import unicode_literals
from django.db import models, migrations
import cryptographic_fields.fields

class Migration(migrations.Migration):
    dependencies = []
    operations = [
     migrations.CreateModel(name=b'TestModel', fields=[
      (
       b'id', models.AutoField(verbose_name=b'ID', serialize=False, auto_created=True, primary_key=True)),
      (
       b'enc_char_field', cryptographic_fields.fields.EncryptedCharField(max_length=396)),
      (
       b'enc_text_field', cryptographic_fields.fields.EncryptedTextField()),
      (
       b'enc_date_field', cryptographic_fields.fields.EncryptedDateField(max_length=100, null=True)),
      (
       b'enc_date_now_field', cryptographic_fields.fields.EncryptedDateField(auto_now=True, max_length=100, null=True)),
      (
       b'enc_date_now_add_field', cryptographic_fields.fields.EncryptedDateField(auto_now_add=True, max_length=100, null=True)),
      (
       b'enc_datetime_field', cryptographic_fields.fields.EncryptedDateTimeField(max_length=100, null=True)),
      (
       b'enc_boolean_field', cryptographic_fields.fields.EncryptedBooleanField(default=True, max_length=100)),
      (
       b'enc_null_boolean_field', cryptographic_fields.fields.EncryptedNullBooleanField(max_length=100)),
      (
       b'enc_integer_field', cryptographic_fields.fields.EncryptedIntegerField(null=True)),
      (
       b'enc_positive_integer_field', cryptographic_fields.fields.EncryptedPositiveIntegerField(null=True)),
      (
       b'enc_small_integer_field', cryptographic_fields.fields.EncryptedSmallIntegerField(null=True)),
      (
       b'enc_positive_small_integer_field', cryptographic_fields.fields.EncryptedPositiveSmallIntegerField(null=True)),
      (
       b'enc_big_integer_field', cryptographic_fields.fields.EncryptedBigIntegerField(null=True))], options={}, bases=(
      models.Model,))]