# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Volumes/Urlugal/Users/geobaldi/src/ripiu/public/github/cmsplugin_rototalc/ripiu/cmsplugin_rototalc/migrations/0002_carouselplugin_initial_slide.py
# Compiled at: 2018-02-20 05:54:07
# Size of source mod 2**32: 530 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('cmsplugin_rototalc', '0001_initial')]
    operations = [
     migrations.AddField(model_name='carouselplugin',
       name='initial_slide',
       field=models.SmallIntegerField(default=0, help_text='Slide to start on.', verbose_name='initial slide'))]