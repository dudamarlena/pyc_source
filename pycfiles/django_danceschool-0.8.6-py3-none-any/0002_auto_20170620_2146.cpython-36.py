# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /c/Users/Lee/Sync/projects/django-danceschool/currentmaster/django-danceschool/danceschool/private_events/migrations/0002_auto_20170620_2146.py
# Compiled at: 2019-04-03 22:56:32
# Size of source mod 2**32: 553 bytes
from __future__ import unicode_literals
import colorful.fields
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
     ('private_events', '0001_initial')]
    operations = [
     migrations.AlterField(model_name='privateeventcategory',
       name='displayColor',
       field=colorful.fields.RGBColorField(default='#0000FF', help_text='Choose a color for the calendar display.'))]