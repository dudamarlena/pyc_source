# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dominicmonn/Documents/Private/cms-sample/dev_packages/djangocms-career/djangocms_career/migrations/0008_auto_20160418_1514.py
# Compiled at: 2016-04-18 09:14:43
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('djangocms_career', '0007_auto_20160418_1325')]
    operations = [
     migrations.AlterField(model_name=b'post', name=b'website', field=models.CharField(help_text=b"Provide a link to the company's website.", max_length=255, null=True, verbose_name=b'Website', blank=True))]