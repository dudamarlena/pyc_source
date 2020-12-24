# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/breno/Envs/djangoplus/lib/python3.7/site-packages/documentos/migrations/0001_initial.py
# Compiled at: 2019-03-20 14:39:48
# Size of source mod 2**32: 3947 bytes
from django.db import migrations, models
import django.db.models.deletion, djangoplus.db.models.fields

class Migration(migrations.Migration):
    initial = True
    dependencies = [
     ('enderecos', '0001_squashed_0006_auto_20170605_2058')]
    operations = [
     migrations.CreateModel(name='Certidao',
       fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'tipo', djangoplus.db.models.fields.CharField(choices=[['Nascimento', 'Nascimento'], ['Casamento', 'Casamento']], max_length=255, verbose_name='Tipo')),
      (
       'numero', djangoplus.db.models.fields.CharField(max_length=255, verbose_name='Número')),
      (
       'cartorio', djangoplus.db.models.fields.CharField(max_length=255, verbose_name='Cartório')),
      (
       'livro', djangoplus.db.models.fields.CharField(max_length=255, verbose_name='Livro')),
      (
       'folha', djangoplus.db.models.fields.CharField(max_length=255, verbose_name='Folha')),
      (
       'data', djangoplus.db.models.fields.DateField(verbose_name='Data')),
      (
       'municipio', djangoplus.db.models.fields.ForeignKey(on_delete=(django.db.models.deletion.CASCADE), to='enderecos.Municipio', verbose_name='Município'))],
       options={'verbose_name':'Certidão', 
      'verbose_name_plural':'Certidões'}),
     migrations.CreateModel(name='CertificadoMilitar',
       fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'numero', djangoplus.db.models.fields.CharField(max_length=255, verbose_name='Número')),
      (
       'serie', djangoplus.db.models.fields.CharField(max_length=255, verbose_name='Série')),
      (
       'categoria', djangoplus.db.models.fields.CharField(blank=True, max_length=255, null=True, verbose_name='Categoria'))],
       options={'verbose_name':'Certificado Militar', 
      'verbose_name_plural':'Certificado Militars'}),
     migrations.CreateModel(name='RG',
       fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'numero', djangoplus.db.models.fields.CharField(max_length=255, verbose_name='Número')),
      (
       'data', djangoplus.db.models.fields.DateField(verbose_name='Data de Expedição')),
      (
       'orgao', djangoplus.db.models.fields.CharField(max_length=255, verbose_name='Orgão Expedidor')),
      (
       'uf', djangoplus.db.models.fields.ForeignKey(on_delete=(django.db.models.deletion.CASCADE), to='enderecos.Estado', verbose_name='UF'))],
       options={'verbose_name':'RG', 
      'verbose_name_plural':'RGs'}),
     migrations.CreateModel(name='TituloEleitor',
       fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'numero', djangoplus.db.models.fields.IntegerField(verbose_name='Número')),
      (
       'zona', djangoplus.db.models.fields.CharField(max_length=255, verbose_name='Zona')),
      (
       'secao', djangoplus.db.models.fields.CharField(max_length=255, verbose_name='Seção')),
      (
       'municipio', djangoplus.db.models.fields.ForeignKey(on_delete=(django.db.models.deletion.CASCADE), to='enderecos.Municipio', verbose_name='Município'))],
       options={'verbose_name':'Título de Eleitor', 
      'verbose_name_plural':'Títulos de Eleitores'})]