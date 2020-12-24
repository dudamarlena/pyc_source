# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ggg/www/dev/mogos/mogo51/mogo/alapage/migrations/0002_page_slideshow_group.py
# Compiled at: 2017-06-14 08:45:07
# Size of source mod 2**32: 621 bytes
from __future__ import unicode_literals
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('jssor', '0001_initial'),
     ('alapage', '0001_initial')]
    operations = [
     migrations.AddField(model_name='page', name='slideshow_group', field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='jssor.ResponsiveGroup', verbose_name='Slideshow'))]