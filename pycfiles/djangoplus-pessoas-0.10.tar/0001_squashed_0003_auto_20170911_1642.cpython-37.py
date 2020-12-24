# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/breno/Envs/djangoplus/lib/python3.7/site-packages/pessoas/migrations/0001_squashed_0003_auto_20170911_1642.py
# Compiled at: 2018-10-05 12:53:22
# Size of source mod 2**32: 1682 bytes
from django.db import migrations, models
import django.db.models.deletion, djangoplus.db.models.fields

class Migration(migrations.Migration):
    replaces = [
     ('pessoas', '0001_initial'), ('pessoas', '0002_pessoa_tipo'), ('pessoas', '0003_auto_20170911_1642')]
    initial = True
    dependencies = [
     ('enderecos', '0006_auto_20170605_2058')]
    operations = [
     migrations.CreateModel(name='Pessoa',
       fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'nome', djangoplus.db.models.fields.CharField(max_length=255, verbose_name='Nome')),
      (
       'documento', djangoplus.db.models.fields.CharField(max_length=255, null=True, verbose_name='Documento')),
      (
       'telefone', djangoplus.db.models.fields.PhoneField(blank=True, max_length=255, null=True, verbose_name='Telefone')),
      (
       'email', djangoplus.db.models.fields.EmailField(blank=True, max_length=255, null=True, verbose_name='E-mail')),
      (
       'endereco', djangoplus.db.models.fields.OneToOneField(blank=True, null=True, on_delete=(django.db.models.deletion.SET_NULL), to='enderecos.Endereco', verbose_name='Endereço')),
      (
       'tipo', djangoplus.db.models.fields.CharField(choices=[['Física', 'Física'], ['Jurídica', 'Jurídica']], max_length=255, null=True, verbose_name='Tipo'))],
       options={'verbose_name':'Pessoa', 
      'verbose_name_plural':'Pessoas'})]