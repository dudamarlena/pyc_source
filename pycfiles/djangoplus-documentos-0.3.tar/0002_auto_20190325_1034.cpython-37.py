# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/breno/Envs/djangoplus/lib/python3.7/site-packages/documentos/migrations/0002_auto_20190325_1034.py
# Compiled at: 2019-03-25 10:13:41
# Size of source mod 2**32: 1740 bytes
from django.db import migrations
import django.db.models.deletion, djangoplus.db.models.fields

class Migration(migrations.Migration):
    dependencies = [
     ('documentos', '0001_initial')]
    operations = [
     migrations.AlterField(model_name='certidao',
       name='cartorio',
       field=djangoplus.db.models.fields.CharField(blank=True, max_length=255, null=True, verbose_name='Cartório')),
     migrations.AlterField(model_name='certidao',
       name='data',
       field=djangoplus.db.models.fields.DateField(blank=True, null=True, verbose_name='Data')),
     migrations.AlterField(model_name='certidao',
       name='folha',
       field=djangoplus.db.models.fields.CharField(blank=True, max_length=255, null=True, verbose_name='Folha')),
     migrations.AlterField(model_name='certidao',
       name='livro',
       field=djangoplus.db.models.fields.CharField(blank=True, max_length=255, null=True, verbose_name='Livro')),
     migrations.AlterField(model_name='certidao',
       name='municipio',
       field=djangoplus.db.models.fields.ForeignKey(null=True, blank=True, on_delete=(django.db.models.deletion.CASCADE), to='enderecos.Municipio', verbose_name='Município')),
     migrations.AlterField(model_name='certidao',
       name='tipo',
       field=djangoplus.db.models.fields.CharField(choices=[['Nascimento', 'Nascimento'], ['Casamento', 'Casamento'], ['Novo Modelo', 'Novo Modelo']], max_length=255, verbose_name='Tipo'))]