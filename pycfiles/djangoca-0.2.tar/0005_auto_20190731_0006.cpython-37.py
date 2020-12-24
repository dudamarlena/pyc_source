# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/oliver/Documentos/Proyectos/base_django/aplicaciones/base/migrations/0005_auto_20190731_0006.py
# Compiled at: 2019-07-31 01:06:53
# Size of source mod 2**32: 400 bytes
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('base', '0004_auto_20190730_2359')]
    operations = [
     migrations.AlterField(model_name='persona',
       name='id',
       field=models.AutoField(primary_key=True, serialize=False))]