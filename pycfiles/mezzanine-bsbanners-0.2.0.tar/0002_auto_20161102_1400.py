# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/home/alan/projects/mldemo-po/mezzanine_bsbanners/migrations/0002_auto_20161102_1400.py
# Compiled at: 2018-11-16 08:16:10
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('mezzanine_bsbanners', '0001_initial')]
    operations = [
     migrations.AlterField(model_name=b'banners', name=b'bannertype', field=models.SmallIntegerField(choices=[(1, 'Carousel'), (2, 'Jumbotron'), (3, 'Image')], default=1))]