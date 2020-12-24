# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/jmbo/migrations/0005_modelbase_layers.py
# Compiled at: 2017-05-03 05:57:29
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('layers', '0002_auto_20161219_1041'),
     ('jmbo', '0004_photosize_name_length')]
    operations = [
     migrations.AddField(model_name=b'modelbase', name=b'layers', field=models.ManyToManyField(blank=True, help_text=b'Makes item eligible to be published on selected layers.', null=True, to=b'layers.Layer'))]