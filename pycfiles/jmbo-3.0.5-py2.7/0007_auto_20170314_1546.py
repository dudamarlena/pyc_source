# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/jmbo/migrations/0007_auto_20170314_1546.py
# Compiled at: 2017-05-03 05:57:29
from __future__ import unicode_literals
from django.db import migrations, models
import photologue.models

class Migration(migrations.Migration):
    dependencies = [
     ('jmbo', '0006_auto_20170206_1337')]
    operations = [
     migrations.AlterField(model_name=b'imageoverride', name=b'replacement', field=models.ImageField(upload_to=photologue.models.get_storage_path))]