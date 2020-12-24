# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/www.django/makarthy/codenerix_transports/migrations/0001_initial.py
# Compiled at: 2017-11-10 07:52:44
# Size of source mod 2**32: 2701 bytes
from __future__ import unicode_literals
from django.db import migrations, models
import django_countries.fields

class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
     migrations.CreateModel(name='TransportRequest', fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
      (
       'updated', models.DateTimeField(auto_now=True, verbose_name='Updated')),
      (
       'ref', models.CharField(default=None, max_length=15, null=True, verbose_name='Referencia')),
      (
       'reverse', models.CharField(max_length=64, verbose_name='Reverse')),
      (
       'platform', models.CharField(max_length=20, verbose_name='Plataforma')),
      (
       'protocol', models.CharField(choices=[('mrw', 'MRW'), ('seur', 'SEUR')], max_length=10, verbose_name='Protocol')),
      (
       'real', models.BooleanField(default=False, verbose_name='Real')),
      (
       'error', models.BooleanField(default=False, verbose_name='Error')),
      (
       'error_txt', models.TextField(blank=True, null=True, verbose_name='Error del text')),
      (
       'cancelled', models.BooleanField(default=False, verbose_name='Cancelado')),
      (
       'notes', models.CharField(blank=True, max_length=30, null=True, verbose_name='Notas')),
      (
       'origin_address', models.CharField(blank=True, max_length=30, null=True, verbose_name='Origin Address')),
      (
       'origin_country', django_countries.fields.CountryField(max_length=2, verbose_name='Origin Country')),
      (
       'destination_address', models.CharField(blank=True, max_length=30, null=True, verbose_name='Destination Address')),
      (
       'destination_country', django_countries.fields.CountryField(max_length=2, verbose_name='Destination Country')),
      (
       'request', models.TextField(blank=True, null=True, verbose_name='Solicitud')),
      (
       'answer', models.TextField(blank=True, null=True, verbose_name='Respuesta')),
      (
       'request_date', models.DateTimeField(blank=True, editable=False, null=True, verbose_name='Fecha de solicitud')),
      (
       'answer_date', models.DateTimeField(blank=True, editable=False, null=True, verbose_name='Fecha de respuesta'))]),
     migrations.AlterUniqueTogether(name='transportrequest', unique_together=set([('ref', 'platform')]))]