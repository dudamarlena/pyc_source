# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Volumes/Urlugal/Users/geobaldi/src/ripiu/public/github/cmsplugin_rototalc/ripiu/cmsplugin_rototalc/migrations/0005_auto_20180222_1602.py
# Compiled at: 2018-02-22 10:02:02
# Size of source mod 2**32: 777 bytes
from __future__ import unicode_literals
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
     ('cmsplugin_rototalc', '0004_carouselplugin_header_alignment')]
    operations = [
     migrations.RemoveField(model_name='carouselplugin',
       name='header_alignment'),
     migrations.RemoveField(model_name='carouselplugin',
       name='heading_level'),
     migrations.RemoveField(model_name='carouselplugin',
       name='subtitle'),
     migrations.RemoveField(model_name='carouselplugin',
       name='title')]