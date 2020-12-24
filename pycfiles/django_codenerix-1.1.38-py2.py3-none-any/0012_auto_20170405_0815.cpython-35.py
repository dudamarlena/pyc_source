# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/www.django/makarthy/codenerix/migrations/0012_auto_20170405_0815.py
# Compiled at: 2017-11-28 06:03:36
# Size of source mod 2**32: 548 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('codenerix', '0011_delete_corporateimage')]
    operations = [
     migrations.AlterField(model_name='log', name='action_flag', field=models.PositiveSmallIntegerField(choices=[(1, 'Añadir'), (2, 'Modificar'), (3, 'Eliminar')], verbose_name='Acción'))]