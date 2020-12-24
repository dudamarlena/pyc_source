# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /webapp/bulbs/special_coverage/migrations/0010_auto_20160407_1705.py
# Compiled at: 2016-09-22 15:00:17
# Size of source mod 2**32: 528 bytes
from __future__ import unicode_literals
from django.db import migrations, models
import djbetty.fields

class Migration(migrations.Migration):
    dependencies = [
     ('special_coverage', '0009_auto_20160208_1540')]
    operations = [
     migrations.AlterField(model_name='specialcoverage', name='image', field=djbetty.fields.ImageField(caption_field='_image_caption', default=None, null=True, alt_field='_image_alt', blank=True))]