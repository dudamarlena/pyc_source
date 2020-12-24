# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/oliver/Documentos/Proyectos/base_django/aplicaciones/base/migrations/0004_auto_20190730_2359.py
# Compiled at: 2019-07-31 00:59:15
# Size of source mod 2**32: 575 bytes
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('base', '0003_hombre_persona')]
    operations = [
     migrations.AddField(model_name='persona',
       name='estado',
       field=models.BooleanField(default=True)),
     migrations.AlterField(model_name='persona',
       name='apellidos',
       field=models.CharField(max_length=200, verbose_name='Apellidos de Persona'))]