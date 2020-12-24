# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /libs/django_brfied/django_brfied/migrations/0001_initial.py
# Compiled at: 2019-02-27 18:19:34
# Size of source mod 2**32: 1730 bytes
from django.db import migrations, models
import django_brfied.models

class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
     migrations.CreateModel(name='Municipio',
       fields=[
      (
       'codigo', models.CharField(max_length=6, primary_key=True, serialize=False, verbose_name='Código')),
      (
       'nome', models.CharField(max_length=255, verbose_name='Código'))],
       options={'verbose_name':'Município', 
      'verbose_name_plural':'Municípios', 
      'ordering':[
       'nome']}),
     migrations.CreateModel(name='UnidadeFederativa',
       fields=[
      (
       'sigla', models.CharField(max_length=2, primary_key=True, serialize=False, verbose_name='Sigla')),
      (
       'codigo', models.CharField(max_length=2, unique=True, verbose_name='Código')),
      (
       'nome', models.CharField(max_length=250, verbose_name='Nome')),
      (
       'regiao', models.CharField(choices=[('N', 'Norte'), ('NE', 'Nordeste'), ('SE', 'Sudeste'), ('S', 'Sul'), ('CO', 'Centro-Oeste')], max_length=2, verbose_name='Região'))],
       options={'verbose_name':'Unidade federativa', 
      'verbose_name_plural':'Unidades federativas', 
      'ordering':[
       'nome']}),
     migrations.AddField(model_name='municipio',
       name='uf',
       field=django_brfied.models.UFField(on_delete=None, to='django_brfied.UnidadeFederativa', verbose_name='UF'))]