# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Volumes/Urlugal/Users/geobaldi/src/ripiu/public/github/cmsplugin_fup/ripiu/cmsplugin_fup/migrations/0003_auto_20180409_1325.py
# Compiled at: 2018-04-10 05:23:33
# Size of source mod 2**32: 1396 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('cmsplugin_fup', '0002_auto_20171019_1021')]
    operations = [
     migrations.AlterField(model_name='fupitempluginmodel',
       name='height_unit',
       field=models.CharField(choices=[('vh', 'vh'), ('vw', 'vw'), ('px', 'pixel'), ('rem', 'root em'), ('%', '%')], max_length=5, verbose_name='unit')),
     migrations.AlterField(model_name='fupitempluginmodel',
       name='width_unit',
       field=models.CharField(choices=[('vw', 'vw'), ('vh', 'vh'), ('px', 'pixel'), ('rem', 'root em'), ('%', '%')], max_length=5, verbose_name='unit')),
     migrations.AlterField(model_name='fupitemposition',
       name='x_unit',
       field=models.CharField(choices=[('vw', 'vw'), ('vh', 'vh'), ('px', 'pixel'), ('rem', 'root em'), ('%', '%')], max_length=5, verbose_name='unit')),
     migrations.AlterField(model_name='fupitemposition',
       name='y_unit',
       field=models.CharField(choices=[('vh', 'vh'), ('vw', 'vw'), ('px', 'pixel'), ('rem', 'root em'), ('%', '%')], max_length=5, verbose_name='unit'))]