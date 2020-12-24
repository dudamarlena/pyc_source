# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /mnt/c/django-danceschool/currentmaster/django-danceschool/danceschool/core/migrations/0007_auto_20170620_2146.py
# Compiled at: 2018-03-26 19:55:26
# Size of source mod 2**32: 908 bytes
from __future__ import unicode_literals
import colorful.fields, danceschool.core.models
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
     ('core', '0006_remove_dancetypelevel_requiresaudition')]
    operations = [
     migrations.AlterField(model_name='dancetypelevel', name='displayColor', field=colorful.fields.RGBColorField(default=danceschool.core.models.get_defaultClassColor, help_text='Choose a color for the calendar display.', verbose_name='Display Color')),
     migrations.AlterField(model_name='publiceventcategory', name='displayColor', field=colorful.fields.RGBColorField(default='#0000FF', help_text='Choose a color for the calendar display.'))]