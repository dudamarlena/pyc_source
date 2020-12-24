# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/breno/Envs/djangoplus/lib/python3.7/site-packages/djangoplus/admin/migrations/0002_log_logindex.py
# Compiled at: 2018-10-05 12:53:01
# Size of source mod 2**32: 2483 bytes
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion, djangoplus.db.models.fields

class Migration(migrations.Migration):
    dependencies = [
     ('contenttypes', '0002_remove_content_type_name'),
     ('admin', '0001_initial')]
    operations = [
     migrations.CreateModel(name='Log',
       fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'operation', djangoplus.db.models.fields.IntegerField(choices=[[1, 'Cadastro'], [2, 'Edição'], [3, 'Exclusão']], verbose_name='Operação')),
      (
       'date', djangoplus.db.models.fields.DateTimeField(auto_now=True, verbose_name='Data/Hora')),
      (
       'object_id', djangoplus.db.models.fields.IntegerField(verbose_name='Identificador')),
      (
       'object_description', djangoplus.db.models.fields.CharField(max_length=255, verbose_name='Descrição do Objeto')),
      (
       'content', djangoplus.db.models.fields.TextField(null=True, verbose_name='Conteúdo')),
      (
       'content_type', djangoplus.db.models.fields.ModelChoiceField(on_delete=(django.db.models.deletion.CASCADE), to='contenttypes.ContentType', verbose_name='Objeto')),
      (
       'user', djangoplus.db.models.fields.ModelChoiceField(on_delete=(django.db.models.deletion.CASCADE), to=(settings.AUTH_USER_MODEL)))],
       options={'verbose_name':'Log', 
      'verbose_name_plural':'Logs'}),
     migrations.CreateModel(name='LogIndex',
       fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'object_id', djangoplus.db.models.fields.IntegerField(verbose_name='Identificador')),
      (
       'content_type', djangoplus.db.models.fields.ModelChoiceField(on_delete=(django.db.models.deletion.CASCADE), to='contenttypes.ContentType', verbose_name='Dado')),
      (
       'log', djangoplus.db.models.fields.ModelChoiceField(on_delete=(django.db.models.deletion.CASCADE), to='admin.Log', verbose_name='Log'))],
       options={'verbose_name':'Index', 
      'verbose_name_plural':'Indexes'})]