# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/rowan/Nyaruka/dash/dash_test_runner/testapp/migrations/0003_auto_20180405_1238.py
# Compiled at: 2018-08-14 12:18:01
# Size of source mod 2**32: 406 bytes
import django.db.models.deletion
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('testapp', '0002_auto_20180312_1302')]
    operations = [
     migrations.AlterField(model_name='contact',
       name='backend',
       field=models.ForeignKey(on_delete=(models.PROTECT), to='orgs.OrgBackend'))]