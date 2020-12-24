# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /webapp/bulbs/special_coverage/migrations/0006_auto_20151109_1708.py
# Compiled at: 2016-09-22 15:00:17
# Size of source mod 2**32: 940 bytes
from __future__ import unicode_literals
from django.db import migrations, models
import djbetty.fields

class Migration(migrations.Migration):
    dependencies = [
     ('special_coverage', '0005_auto_20151103_1358')]
    operations = [
     migrations.AddField(model_name='specialcoverage', name='_image_alt', field=models.CharField(max_length=255, null=True, editable=False, blank=True)),
     migrations.AddField(model_name='specialcoverage', name='_image_caption', field=models.CharField(max_length=255, null=True, editable=False, blank=True)),
     migrations.AddField(model_name='specialcoverage', name='image', field=djbetty.fields.ImageField(default=None, alt_field=b'_image_alt', null=True, caption_field=b'_image_caption', blank=True))]