# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/geobaldi/src/ripiu/public/ripiu.cmsplugin_lasagna/ripiu/cmsplugin_lasagna/migrations/0003_auto_20180108_0036.py
# Compiled at: 2018-01-07 18:36:01
# Size of source mod 2**32: 1021 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('cmsplugin_lasagna', '0002_auto_20180102_1844')]
    operations = [
     migrations.AlterField(model_name='imageanchormodifierplugin',
       name='object_fit',
       field=models.CharField(choices=[('fill', 'Fill the container'), ('contain', 'Fit into the container'), ('cover', 'Fill the container and maintain the aspect ratio'), ('none', "Don't resize"), ('scale-down', 'Scale down to fit into the container')], default='cover', max_length=10, verbose_name='resize')),
     migrations.AlterField(model_name='verticalalignmentmodifierplugin',
       name='alignment',
       field=models.PositiveSmallIntegerField(choices=[(0, 'top'), (1, 'middle'), (2, 'bottom')], default=0, verbose_name='alignment'))]