# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/bfschott/Source/cmsplugin-newsplus/cmsplugin_newsplus/migrations/0002_auto_20150428_1335.py
# Compiled at: 2016-06-07 17:28:14
from __future__ import unicode_literals
from django.db import models, migrations
import django.utils.timezone

class Migration(migrations.Migration):
    dependencies = [
     ('cmsplugin_newsplus', '0001_initial')]
    operations = [
     migrations.AlterField(model_name=b'news', name=b'pub_date', field=models.DateTimeField(default=django.utils.timezone.now, verbose_name=b'Publication date'), preserve_default=True)]