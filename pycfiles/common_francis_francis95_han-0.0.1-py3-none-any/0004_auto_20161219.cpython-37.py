# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/marc/Git/common-framework/common/migrations/0004_auto_20161219.py
# Compiled at: 2018-02-03 12:24:20
# Size of source mod 2**32: 470 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('common', '0003_auto_20160801')]
    operations = [
     migrations.AlterField(model_name='serviceusage',
       name='name',
       field=models.CharField(max_length=200, verbose_name='nom'))]