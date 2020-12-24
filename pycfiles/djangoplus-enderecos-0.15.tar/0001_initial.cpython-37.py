# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/breno/Envs/djangoplus/lib/python3.7/site-packages/enderecos/migrations/0001_initial.py
# Compiled at: 2018-10-05 12:52:35
# Size of source mod 2**32: 5246 bytes
from django.db import migrations, models
import django.db.models.deletion, djangoplus.db.models.fields

class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
     migrations.CreateModel(name='Bairro',
       fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'nome', djangoplus.db.models.fields.CharField(max_length=255, verbose_name='Nome')),
      (
       'codigo', djangoplus.db.models.fields.CharField(max_length=255, verbose_name='Código'))],
       options={'verbose_name':'Bairro', 
      'verbose_name_plural':'Bairros'}),
     migrations.CreateModel(name='Endereco',
       fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'logradouro', djangoplus.db.models.fields.CharField(max_length=255, verbose_name='Logradouro')),
      (
       'numero', djangoplus.db.models.fields.IntegerField(verbose_name='Número')),
      (
       'complemento', djangoplus.db.models.fields.CharField(blank=True, max_length=255, null=True, verbose_name='Complemento')),
      (
       'cep', djangoplus.db.models.fields.CepField(blank=True, max_length=255, null=True, verbose_name='CEP')),
      (
       'bairro', djangoplus.db.models.fields.ForeignKey(on_delete=(django.db.models.deletion.CASCADE), to='enderecos.Bairro', verbose_name='Bairro'))],
       options={'verbose_name':'Endereço', 
      'verbose_name_plural':'Endereços'}),
     migrations.CreateModel(name='Estado',
       fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'nome', djangoplus.db.models.fields.CharField(max_length=255, verbose_name='Nome')),
      (
       'sigla', djangoplus.db.models.fields.CharField(max_length=255, verbose_name='Sigla')),
      (
       'codigo', djangoplus.db.models.fields.CharField(max_length=255, verbose_name='Código'))],
       options={'verbose_name':'Estado', 
      'verbose_name_plural':'Estados'}),
     migrations.CreateModel(name='Municipio',
       fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'nome', djangoplus.db.models.fields.CharField(max_length=255, verbose_name='Nome')),
      (
       'codigo', djangoplus.db.models.fields.CharField(max_length=255, verbose_name='Código')),
      (
       'estado', djangoplus.db.models.fields.ForeignKey(on_delete=(django.db.models.deletion.CASCADE), to='enderecos.Estado', verbose_name='Estado'))],
       options={'verbose_name':'Município', 
      'verbose_name_plural':'Municípios'}),
     migrations.CreateModel(name='Regiao',
       fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'nome', djangoplus.db.models.fields.CharField(max_length=255, verbose_name='Nome')),
      (
       'codigo', djangoplus.db.models.fields.CharField(max_length=255, verbose_name='Código'))],
       options={'verbose_name':'Região', 
      'verbose_name_plural':'Regiões'}),
     migrations.CreateModel(name='Telefone',
       fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'tipo', djangoplus.db.models.fields.CharField(choices=[('Residencial', 'Residencial'), ('Profissional', 'Profissional')], max_length=255, verbose_name='Tipo')),
      (
       'numero', djangoplus.db.models.fields.PhoneField(max_length=255, verbose_name='Número'))],
       options={'verbose_name':'Telefone', 
      'verbose_name_plural':'Telefones'}),
     migrations.AddField(model_name='estado',
       name='regiao',
       field=djangoplus.db.models.fields.ForeignKey(null=True, on_delete=(django.db.models.deletion.CASCADE), to='enderecos.Regiao', verbose_name='Região')),
     migrations.AddField(model_name='endereco',
       name='municipio',
       field=djangoplus.db.models.fields.ForeignKey(on_delete=(django.db.models.deletion.CASCADE), to='enderecos.Municipio', verbose_name='Município')),
     migrations.AddField(model_name='bairro',
       name='cidade',
       field=djangoplus.db.models.fields.ForeignKey(on_delete=(django.db.models.deletion.CASCADE), to='enderecos.Municipio', verbose_name='Município'))]