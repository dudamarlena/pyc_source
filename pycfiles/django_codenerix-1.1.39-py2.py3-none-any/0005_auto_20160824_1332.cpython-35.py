# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/www.django/makarthy/codenerix/migrations/0005_auto_20160824_1332.py
# Compiled at: 2017-11-28 06:03:36
# Size of source mod 2**32: 433 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('codenerix', '0004_auto_20160824_0757')]
    operations = [
     migrations.AlterField(model_name='log', name='action_flag', field=models.PositiveSmallIntegerField(verbose_name='Acción'))]