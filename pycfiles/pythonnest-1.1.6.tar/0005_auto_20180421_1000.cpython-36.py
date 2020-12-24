# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/flanker/Developer/Github/PythonNest/pythonnest/migrations/0005_auto_20180421_1000.py
# Compiled at: 2018-04-21 04:01:00
# Size of source mod 2**32: 568 bytes
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('pythonnest', '0004_auto_20160117_1805')]
    operations = [
     migrations.AlterField(model_name='package',
       name='group',
       field=models.ForeignKey(blank=True, null=True, on_delete=(django.db.models.deletion.SET_NULL), to='auth.Group',
       verbose_name='restrict to this group'))]