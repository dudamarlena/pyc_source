# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Volumes/Urlugal/Users/geobaldi/src/github/ripiu.cmsplugin_columns/ripiu/cmsplugin_columns/migrations/0002_auto_20171003_1255.py
# Compiled at: 2017-10-03 06:55:01
# Size of source mod 2**32: 618 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('cmsplugin_columns', '0001_initial')]
    operations = [
     migrations.AlterField(model_name='liquidcolumnspluginmodel',
       name='num_columns',
       field=models.IntegerField(choices=[(2, 'Two'), (3, 'Three'), (4, 'Four'), (5, 'Five'), (6, 'Six')], default=2, help_text='How many columns for this section?', verbose_name='columns'))]