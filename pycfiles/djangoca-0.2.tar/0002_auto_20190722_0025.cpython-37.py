# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/oliver/Documentos/Proyectos/base_django/aplicaciones/usuarios/migrations/0002_auto_20190722_0025.py
# Compiled at: 2019-07-22 01:25:21
# Size of source mod 2**32: 393 bytes
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('usuarios', '0001_initial')]
    operations = [
     migrations.AlterField(model_name='usuario',
       name='id',
       field=models.AutoField(primary_key=True, serialize=False))]