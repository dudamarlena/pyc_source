# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/www.django/makarthy/codenerix/migrations/0002_auto_20160808_0843.py
# Compiled at: 2017-11-28 06:03:36
# Size of source mod 2**32: 421 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('codenerix', '0001_initial')]
    operations = [
     migrations.AlterField(model_name='log', name='action_time', field=models.DateTimeField(auto_now=True, verbose_name='Fecha'))]