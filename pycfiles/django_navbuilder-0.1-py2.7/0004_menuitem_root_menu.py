# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/navbuilder/migrations/0004_menuitem_root_menu.py
# Compiled at: 2017-07-06 08:35:55
from __future__ import unicode_literals
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('navbuilder', '0003_auto_20161017_1414')]
    operations = [
     migrations.AddField(model_name=b'menuitem', name=b'root_menu', field=models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, to=b'navbuilder.Menu'))]