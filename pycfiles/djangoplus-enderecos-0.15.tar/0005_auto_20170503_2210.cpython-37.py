# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/breno/Envs/djangoplus/lib/python3.7/site-packages/enderecos/migrations/0005_auto_20170503_2210.py
# Compiled at: 2018-10-05 12:52:35
# Size of source mod 2**32: 904 bytes
from django.db import migrations
import djangoplus.db.models.fields

class Migration(migrations.Migration):
    dependencies = [
     ('enderecos', '0004_auto_20170503_1923')]
    operations = [
     migrations.RemoveField(model_name='bairro',
       name='municipio'),
     migrations.AlterField(model_name='endereco',
       name='bairro',
       field=djangoplus.db.models.fields.CharField(max_length=255, verbose_name='Bairro')),
     migrations.AlterField(model_name='endereco',
       name='cep',
       field=djangoplus.db.models.fields.CepField(default='', max_length=255, verbose_name='CEP'),
       preserve_default=False),
     migrations.DeleteModel(name='Bairro')]