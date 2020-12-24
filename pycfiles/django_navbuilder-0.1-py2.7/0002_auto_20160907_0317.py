# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/navbuilder/migrations/0002_auto_20160907_0317.py
# Compiled at: 2017-01-25 06:30:30
from __future__ import unicode_literals
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('contenttypes', '0002_remove_content_type_name'),
     ('navbuilder', '0001_initial')]
    operations = [
     migrations.RemoveField(model_name=b'menuitem', name=b'link'),
     migrations.AddField(model_name=b'menuitem', name=b'link_content_type', field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=b'contenttypes.ContentType')),
     migrations.AddField(model_name=b'menuitem', name=b'link_object_id', field=models.PositiveIntegerField(null=True)),
     migrations.AlterField(model_name=b'menuitem', name=b'menu', field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name=b'menuitems', to=b'navbuilder.Menu'))]