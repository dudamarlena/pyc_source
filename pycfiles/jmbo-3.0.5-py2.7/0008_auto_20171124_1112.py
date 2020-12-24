# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/jmbo/migrations/0008_auto_20171124_1112.py
# Compiled at: 2018-01-02 08:02:08
from __future__ import unicode_literals
from django.db import migrations
import sortedm2m.fields

class Migration(migrations.Migration):
    dependencies = [
     ('jmbo', '0007_auto_20170314_1546')]
    operations = [
     migrations.AlterField(model_name=b'modelbase', name=b'images', field=sortedm2m.fields.SortedManyToManyField(blank=True, help_text=None, null=True, sort_value_field_name=b'position', through=b'jmbo.ModelBaseImage', to=b'jmbo.Image'))]