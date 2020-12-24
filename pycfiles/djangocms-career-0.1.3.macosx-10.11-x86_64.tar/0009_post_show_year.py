# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dominicmonn/Documents/Private/dev_packages/djangocms-career/djangocms_career/migrations/0009_post_show_year.py
# Compiled at: 2016-08-26 15:17:46
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('djangocms_career', '0008_auto_20160418_1514')]
    operations = [
     migrations.AddField(model_name=b'post', name=b'show_year', field=models.BooleanField(default=False, help_text=b'Displays how long the current position was held.', verbose_name=b'Show Year'))]