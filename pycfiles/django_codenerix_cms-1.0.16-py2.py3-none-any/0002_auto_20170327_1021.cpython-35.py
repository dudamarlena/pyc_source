# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/www.django/makarthy/codenerix_cms/migrations/0002_auto_20170327_1021.py
# Compiled at: 2017-11-28 07:16:52
# Size of source mod 2**32: 741 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('codenerix_cms', '0001_initial')]
    operations = [
     migrations.AlterField(model_name='slider', name='identifier', field=models.CharField(blank=True, max_length=200, null=True, unique=True, verbose_name='Identifier')),
     migrations.AlterField(model_name='staticheader', name='identifier', field=models.CharField(blank=True, max_length=200, null=True, unique=True, verbose_name='Identifier'))]