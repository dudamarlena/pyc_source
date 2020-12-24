# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/navbuilder/migrations/0003_auto_20161017_1414.py
# Compiled at: 2017-07-06 08:35:55
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('navbuilder', '0002_auto_20160907_0317')]
    operations = [
     migrations.AlterModelOptions(name=b'menuitem', options={b'ordering': [b'position']}),
     migrations.AddField(model_name=b'menuitem', name=b'target', field=models.CharField(blank=True, choices=[('blank', '_blank'), ('parent', '_parent'), ('top', '_top'), ('self', '_self')], max_length=256, null=True))]