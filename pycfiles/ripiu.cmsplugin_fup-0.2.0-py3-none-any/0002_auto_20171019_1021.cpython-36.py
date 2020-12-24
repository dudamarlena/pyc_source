# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Volumes/Urlugal/Users/geobaldi/src/ripiu/public/github/cmsplugin_fup/ripiu/cmsplugin_fup/migrations/0002_auto_20171019_1021.py
# Compiled at: 2018-02-20 05:53:30
# Size of source mod 2**32: 707 bytes
from __future__ import unicode_literals
from django.db import models, migrations

class Migration(migrations.Migration):
    dependencies = [
     ('cmsplugin_fup', '0001_initial')]
    operations = [
     migrations.AlterField(model_name='fupitempluginmodel',
       name='height',
       field=models.DecimalField(decimal_places=2, max_digits=5, verbose_name='height')),
     migrations.AlterField(model_name='fupitempluginmodel',
       name='width',
       field=models.DecimalField(decimal_places=2, max_digits=5, verbose_name='width'))]