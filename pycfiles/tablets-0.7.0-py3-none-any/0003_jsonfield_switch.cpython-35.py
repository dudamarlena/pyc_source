# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/craiglabenz/Sites/tablets/tablets/migrations/0003_jsonfield_switch.py
# Compiled at: 2016-10-06 11:52:07
# Size of source mod 2**32: 850 bytes
from __future__ import unicode_literals
from django.db import migrations
import jsonfield.fields

class Migration(migrations.Migration):
    dependencies = [
     ('tablets', '0002_add_mptt')]
    operations = [
     migrations.AlterModelOptions(name='template', options={'verbose_name': 'Template', 'verbose_name_plural': 'Templates'}),
     migrations.AlterField(model_name='template', name='default_context', field=jsonfield.fields.JSONField(blank=True, default=dict, help_text='Does not work so well for Jinja2 templates, which throw exceptions for missing values. This can make things tough if your template relies on functions.', verbose_name='Default Context'))]