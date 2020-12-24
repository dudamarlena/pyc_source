# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/breno/Envs/djangoplus/lib/python3.7/site-packages/djangoplus/admin/migrations/0007_auto_20180416_1854.py
# Compiled at: 2018-10-05 12:53:01
# Size of source mod 2**32: 714 bytes
from django.db import migrations

def migrate(apps, schema_editor):
    Organization = apps.get_model('admin', 'Organization')
    Unit = apps.get_model('admin', 'Unit')
    if Organization.__subclasses__() or Unit.__subclasses__():
        print('\nExecute the following command if you are using sqlite3')
        print('echo .dump | sqlite3 sqlite.db > x.sql && sed \'s/"scope_ptr"/"scope_ptr_id"/g\' x.sql > y.sql && rm x.sql sqlite.db && sqlite3 sqlite.db < y.sql && rm y.sql\n')


class Migration(migrations.Migration):
    dependencies = [
     ('admin', '0006_auto_20180416_1058')]
    operations = [
     migrations.RunPython(migrate)]