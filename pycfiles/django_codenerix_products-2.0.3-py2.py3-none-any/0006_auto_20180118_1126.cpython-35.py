# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/www.django/makarthy/codenerix_products/migrations/0006_auto_20180118_1126.py
# Compiled at: 2018-01-18 06:07:54
# Size of source mod 2**32: 1715 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('codenerix_products', '0005_auto_20180118_0739')]
    operations = [
     migrations.AlterField(model_name='brandtexten', name='name', field=models.CharField(default='test', max_length=250, verbose_name='Name'), preserve_default=False),
     migrations.AlterField(model_name='brandtextes', name='name', field=models.CharField(default='test', max_length=250, verbose_name='Name'), preserve_default=False),
     migrations.AlterField(model_name='productfinaltexten', name='name', field=models.CharField(default='test', max_length=250, verbose_name='Name'), preserve_default=False),
     migrations.AlterField(model_name='productfinaltextes', name='name', field=models.CharField(default='test', max_length=250, verbose_name='Name'), preserve_default=False),
     migrations.AlterField(model_name='producttexttexten', name='name', field=models.CharField(default='test', max_length=250, verbose_name='Name'), preserve_default=False),
     migrations.AlterField(model_name='producttexttextes', name='name', field=models.CharField(default='test', max_length=250, verbose_name='Name'), preserve_default=False)]